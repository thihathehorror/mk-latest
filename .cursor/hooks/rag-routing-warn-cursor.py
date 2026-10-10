#!/usr/bin/env python3
"""Cursor preToolUse adapter for the trc-central RAG-routing gate.

Cursor ၏ hook payload / response schema က Claude Code နှင့် ကွဲသောကြောင့်
ဤ adapter က wire format နှစ်ဘက်ကို ပြောင်းပေးပြီး၊ **စည်းမျဉ်း logic ကို
မပွားစေဘဲ** `.claude/hooks/rag-routing-warn.py` ထဲမှ analyse_* တို့ကိုပဲ
ပြန်သုံးသည် (SoT တစ်ခုတည်း — rule drift မဖြစ်စေရန်)။

Wire mapping
------------
in   : Cursor `{tool_name, tool_input, conversation_id, workspace_roots?}`
       Shell → Bash · Grep/Glob အတိုင်း · `MCP:codegraph_explore` → codegraph stand-down
out  : deny  → {"permission": "deny", "user_message": <reason>}
       warn  → {"agent_message": <systemMessage text>}
       pass  → {"agent_message": ""}   # Cursor က empty stdout ကို invalid လို့ယူသည်

Fail-open — exception မှန်သမျှ passthrough ထုတ်ပြီး exit 0 (hook ပျက်လို့
tool call မပိတ်မိစေရန်)။ Sister script: `.claude/hooks/rag-routing-warn.py`။
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GATE_PATH = os.path.join(PROJECT_DIR, ".claude", "hooks", "rag-routing-warn.py")
PASSTHROUGH = {"agent_message": ""}

# Cursor tool name → Claude tool name.
TOOL_MAP = {"Shell": "Bash", "Grep": "Grep", "Glob": "Glob", "Search": "Grep"}
CURSOR_MCP_PREFIX = "MCP:"


def _emit(payload: dict) -> int:
    json.dump(payload, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def _load_gate():
    """Claude gate script ကို module အဖြစ် load (ဖိုင်အမည်မှာ `-` ပါ၍ import မရ)။"""
    spec = importlib.util.spec_from_file_location("trc_rag_gate", GATE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(GATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _session_id(data: dict) -> str:
    for key in ("conversation_id", "sessionId", "session_id"):
        value = data.get(key)
        if value:
            return str(value)
    return str(os.environ.get("CURSOR_SESSION_ID") or "")


def _cwd(data: dict) -> str:
    roots = data.get("workspace_roots")
    if isinstance(roots, list) and roots:
        return str(roots[0])
    return str(data.get("cwd") or os.environ.get("CURSOR_CWD") or PROJECT_DIR)


def _command(tool_input: dict) -> str:
    for key in ("command", "cmd", "CommandLine"):
        value = tool_input.get(key)
        if isinstance(value, str):
            return value
    return ""


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            return _emit(PASSTHROUGH)

        raw_tool = str(data.get("tool_name") or "")
        tool_input = data.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            tool_input = {}

        gate = _load_gate()
        session_id = _session_id(data)
        cwd = _cwd(data)

        # codegraph သုံးပြီးရင် ကျန် session တစ်လျှောက် stand down (Claude ဘက်နှင့် တူ)။
        if raw_tool.startswith(CURSOR_MCP_PREFIX):
            mcp_tool = raw_tool[len(CURSOR_MCP_PREFIX):]
            if mcp_tool.startswith("codegraph") and session_id:
                path = gate._state_path(session_id)
                state = gate._load_state(path)
                state["codegraph_used"] = True
                gate._save_state(path, state)
            return _emit(PASSTHROUGH)

        tool_name = TOOL_MAP.get(raw_tool, "")
        if not tool_name:
            return _emit(PASSTHROUGH)

        if tool_name == "Bash":
            command = _command(tool_input)
            deny, hints = gate.analyse_bash(command)
            opt_out = gate.OPT_OUT in command
            key_input = {"command": command}
        else:
            deny, hints = gate.analyse_search(tool_input)
            opt_out = gate.OPT_OUT in json.dumps(tool_input, ensure_ascii=False)
            key_input = tool_input

        if deny and not opt_out and session_id and gate._index_ready(cwd):
            path = gate._state_path(session_id)
            state = gate._load_state(path)
            nudged = state.get("nudged") or []
            key = gate._call_key(tool_name, key_input)
            if not state.get("codegraph_used") and key not in nudged:
                nudged.append(key)
                state["nudged"] = nudged[-64:]
                gate._save_state(path, state)
                return _emit({"permission": "deny", "user_message": gate.DENY_REASON})
            # ထပ်ခေါ်ပြီး (သို့) codegraph သုံးပြီး — ဖြတ်သန်းခွင့်ပြု။
            return _emit(PASSTHROUGH)

        if deny and not opt_out and not hints:
            # Deny path ကို guard တစ်ခုက ပိတ်ထား — warn သို့ ပြန်ကျ။
            hints = [
                "`.ts`/`.tsx` explore — `codegraph_explore` **အရင်** ခေါ် "
                "(grep+Read loop မလုပ်ရ; source + blast radius တစ်ခါတည်းရ)"
            ]

        if hints:
            msg = (
                "[trc-central routing] "
                + " · ".join(hints)
                + " — CLAUDE.md `Other tool rules` ကြည့်။"
            )
            return _emit({"agent_message": msg})
    except Exception:  # fail-open — hook ပျက်လို့ tool call မပိတ်ရ
        return _emit(PASSTHROUGH)
    return _emit(PASSTHROUGH)


if __name__ == "__main__":
    sys.exit(main())
