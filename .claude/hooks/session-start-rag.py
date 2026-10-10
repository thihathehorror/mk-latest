#!/usr/bin/env python3
"""SessionStart RAG warm-up (Claude Code).

Root-cause fix for "the agent greps instead of calling codegraph": the codegraph
MCP server connects lazily, so the very first tool call of a session often lands
before it is available and the grep+Read habit takes over for the rest of the run.

This hook, at turn 0:
  1. touches the codegraph CLI so the index/server is warm (background, capped),
  2. sweeps stale `claude-rag-gate-*.json` state files left by the PreToolUse gate,
  3. injects the routing table + handoff SoT pointer as `additionalContext`.

Fail-open like its sisters — any exception still exits 0.
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
import sys
import time

STATE_TTL = 24 * 3600

CONTEXT = """[trc-central session routing - see CLAUDE.md `Other tool rules`]
- TS/TSX/JS symbol, flow, "how does X work", blast radius -> call `codegraph_explore` FIRST.
  No grep+Read loop. The PreToolUse gate denies the first ts/tsx grep of a session.
- .scss / .svg / .json / .md / assets -> `rg` or Grep (not in the codegraph index; correct choice).
- build / test / lint / any output over ~20 lines -> `ctx_batch_execute` or `ctx_execute`.
- One file you are about to edit -> native `Read`; create/modify -> `Write`/`Edit` only.
- After resume or compact -> `ctx_search(sort: "timeline")`, then `active_context.md` + `progress.md`.
- Workflow: one `y` unlocks exactly ONE step (Scout -> Architect -> Builder -> QA -> DevOps).
- Replies to the user are Myanmar ONLY; internal reasoning stays English."""


def _sweep_stale_state() -> None:
    tmp = os.environ.get("TMPDIR") or "/tmp"
    now = time.time()
    for path in glob.glob(os.path.join(tmp, "claude-rag-gate-*.json")):
        try:
            if now - os.path.getmtime(path) > STATE_TTL:
                os.remove(path)
        except Exception:
            pass


def _warm_codegraph(cwd: str) -> None:
    exe = shutil.which("codegraph")
    if not exe or not os.path.isfile(os.path.join(cwd, ".codegraph", "codegraph.db")):
        return
    try:
        # Cheap, bounded touch — just enough to page the index in. Never blocks
        # the session: output discarded, hard timeout, failures ignored.
        subprocess.run(
            [exe, "status", cwd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=8,
            check=False,
        )
    except Exception:
        pass


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        cwd = str(data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ".")

        _sweep_stale_state()
        _warm_codegraph(cwd)

        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": CONTEXT,
                }
            },
            sys.stdout,
        )
        sys.stdout.write("\n")
    except Exception:  # fail-open
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
