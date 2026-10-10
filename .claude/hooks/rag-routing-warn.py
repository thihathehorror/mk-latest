#!/usr/bin/env python3
"""PreToolUse RAG-routing gate (Claude Code).

Two behaviours, both fail-open:

1. **One-shot deny** — the FIRST `.ts`/`.tsx` symbol/flow lookup of a session that
   goes to `Grep`/`Glob`/Bash-grep is denied with a pointer to `codegraph_explore`.
   Retrying the same call is allowed (the nudge is recorded per session), so the
   gate never permanently blocks work.
2. **Warn** — everything else CLAUDE.md routes elsewhere (build/test/lint volume →
   `ctx_*`, ambiguous `src/` reads) only gets a `systemMessage` reminder.

Guards on the deny path: codegraph index must exist, the target must carry real
ts/tsx/js evidence, `session_id` must be present, and any exception exits 0.
`# rag-ok` anywhere in the command/pattern opts out.

Sister script of `precompact-handoff-warn.py` and `session-start-rag.py`.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time

# codegraph index scope (.codegraph/codegraph.db `files`): ts/tsx/js/py/mjs only.
# .scss/.svg/.json are NOT indexed — rg is the correct tool for those.
SKIP_EXT = re.compile(r"\.(scss|css|svg|png|webp|json|md|mdc|lock|ya?ml|xml|html)\b", re.I)
READERS = re.compile(r"(?:^|[|;&]\s*)\s*(rg|grep|egrep|ag|sed|cat|head|tail)\b")
TS_TARGET = re.compile(r"\.tsx?\b|--include=\*\.tsx?\b|--type[= ]tsx?\b")
SRC_TARGET = re.compile(r"\bsrc/\S*")
VOLUME = re.compile(r"\b(heft|eslint|tsc)\b|npm\s+(?:run\s+)?(?:build|test|lint)")
# git/file-move plumbing stays on Bash per CLAUDE.md — never warn on it.
PLUMBING = re.compile(r"(?:^|[|;&]\s*)\s*(git|mkdir|rm|mv|cp|ls|which|chmod|touch|npm\s+i)\b")
# A heredoc or an output redirect makes the command a WRITE, not an explore —
# its body routinely mentions `.ts` paths and must never trip the gate.
HEREDOC = re.compile(r"<<-?\s*['\"]?[A-Za-z_]\w*")
WRITE_REDIRECT = re.compile(r"(?:^|[|;&]\s*)\s*(?:cat|tee|printf|echo)\b[^|;&]*?>>?\s*\S")

# Grep/Glob structured-input evidence.
INDEXED_TYPE = {"ts", "tsx", "js", "jsx", "mjs", "py"}
GLOB_TS = re.compile(r"\*\.(tsx?|jsx?|mjs|py)\b|\.(tsx?|jsx?|mjs|py)$", re.I)
GLOB_SKIP = re.compile(r"\*\.(scss|css|svg|json|md|mdc|ya?ml|xml|html|png|webp)\b", re.I)
# A bare identifier / camelCase / dotted member — the classic symbol lookup.
IDENTIFIER = re.compile(r"^[A-Za-z_$][\w$]{2,}(?:\.[A-Za-z_$][\w$]*)*$")

OPT_OUT = "# rag-ok"
STATE_TTL = 24 * 3600

DENY_REASON = (
    "[trc-central RAG gate] `.ts`/`.tsx` symbol / flow / blast-radius lookup — "
    "`codegraph_explore` **အရင်** ခေါ်ပါ (source + caller + blast radius တစ်ခါတည်းရ; "
    "grep+Read loop မလုပ်ရ)။ codegraph မရ (သို့) ဒီ search တကယ်လိုအပ်ရင် "
    "**ဒီ tool call ကို ထပ်ခေါ်လိုက်ပါ — ဒုတိယအကြိမ်မှာ ခွင့်ပြုပါမယ်**။ "
    "Detail: CLAUDE.md `Other tool rules`။"
)


# ---------------------------------------------------------------- state


def _state_path(session_id: str) -> str:
    tmp = os.environ.get("TMPDIR") or "/tmp"
    digest = hashlib.sha1(session_id.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tmp, f"claude-rag-gate-{digest}.json")


def _load_state(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if time.time() - float(data.get("ts", 0)) > STATE_TTL:
            return {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_state(path: str, state: dict) -> None:
    try:
        state["ts"] = time.time()
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
    except Exception:
        pass


def _call_key(tool_name: str, tool_input: dict) -> str:
    keep = {k: tool_input.get(k) for k in ("command", "pattern", "path", "glob", "type")}
    blob = tool_name + "|" + json.dumps(keep, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]


def _index_ready(cwd: str) -> bool:
    return os.path.isfile(os.path.join(cwd or ".", ".codegraph", "codegraph.db"))


# ---------------------------------------------------------------- analysis


def analyse_bash(cmd: str) -> tuple[bool, list[str]]:
    """Return (deny_candidate, warn_hints) for a Bash command."""
    hints: list[str] = []
    if not cmd.strip() or PLUMBING.search(cmd):
        return False, hints
    if HEREDOC.search(cmd) or WRITE_REDIRECT.search(cmd):
        return False, hints

    if VOLUME.search(cmd):
        hints.append(
            "build/test/lint output — `ctx_batch_execute` သို့ `ctx_execute` သုံး "
            "(raw bytes context ထဲ မဝင်စေရန်)"
        )

    if not READERS.search(cmd):
        return False, hints

    # Explicit ts/tsx evidence wins even when a non-indexed extension is also
    # mentioned in the same command line (the old whole-string veto hid these).
    if TS_TARGET.search(cmd):
        return True, hints

    if SRC_TARGET.search(cmd) and not SKIP_EXT.search(cmd):
        hints.append(
            "`src/` explore — `codegraph_explore` **အရင်** ခေါ် "
            "(grep+Read loop မလုပ်ရ; source + blast radius တစ်ခါတည်းရ)"
        )
    return False, hints


def analyse_search(tool_input: dict) -> tuple[bool, list[str]]:
    """Return (deny_candidate, warn_hints) for a Grep / Glob call."""
    pattern = str(tool_input.get("pattern") or "")
    path = str(tool_input.get("path") or "")
    glob = str(tool_input.get("glob") or "")
    ftype = str(tool_input.get("type") or "").lower()

    # Extension evidence outranks the path: `src` + `*.scss` is correctly rg work.
    if GLOB_SKIP.search(glob) or (ftype and ftype not in INDEXED_TYPE):
        return False, []

    if ftype in INDEXED_TYPE or GLOB_TS.search(glob) or GLOB_TS.search(pattern):
        return True, []

    if glob or SKIP_EXT.search(path):
        return False, []

    in_src = (not path) or re.search(r"(^|/)src(/|$)", path) is not None
    if in_src and IDENTIFIER.match(pattern.strip()):
        # Bare symbol sweep with no extension filter — the grep+Read loop shape.
        return True, []

    if in_src and path:
        return False, [
            "`src/` explore — `codegraph_explore` **အရင်** ခေါ် "
            "(grep+Read loop မလုပ်ရ)"
        ]
    return False, []


# ---------------------------------------------------------------- main


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        tool_name = str(data.get("tool_name") or "")
        tool_input = data.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            tool_input = {}
        session_id = str(data.get("session_id") or "")
        cwd = str(data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ".")

        # codegraph was used this session — stand down for the rest of it.
        if tool_name.startswith("mcp__codegraph__"):
            if session_id:
                path = _state_path(session_id)
                state = _load_state(path)
                state["codegraph_used"] = True
                _save_state(path, state)
            return 0

        if tool_name == "Bash":
            deny, hints = analyse_bash(str(tool_input.get("command") or ""))
            opt_out = OPT_OUT in str(tool_input.get("command") or "")
        elif tool_name in ("Grep", "Glob"):
            deny, hints = analyse_search(tool_input)
            opt_out = OPT_OUT in json.dumps(tool_input, ensure_ascii=False)
        else:
            return 0

        if deny and not opt_out and session_id and _index_ready(cwd):
            path = _state_path(session_id)
            state = _load_state(path)
            nudged = state.get("nudged") or []
            key = _call_key(tool_name, tool_input)
            if not state.get("codegraph_used") and key not in nudged:
                nudged.append(key)
                state["nudged"] = nudged[-64:]
                _save_state(path, state)
                json.dump(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": DENY_REASON,
                        }
                    },
                    sys.stdout,
                )
                sys.stdout.write("\n")
                return 0
            # Already nudged (or codegraph already used) — let it through.
            return 0

        if deny and not opt_out and not hints:
            # Deny path disarmed by a guard (no index / no session_id / already
            # nudged) — degrade to the old reminder. An explicit `# rag-ok`
            # opt-out stays fully silent.
            hints = [
                "`.ts`/`.tsx` explore — `codegraph_explore` **အရင်** ခေါ် "
                "(grep+Read loop မလုပ်ရ; source + blast radius တစ်ခါတည်းရ)"
            ]

        if hints:
            msg = "[trc-central routing] " + " · ".join(hints) + " — CLAUDE.md `Other tool rules` ကြည့်။"
            json.dump({"systemMessage": msg}, sys.stdout)
            sys.stdout.write("\n")
    except Exception:  # fail-open — a broken hook must never block a tool call
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
