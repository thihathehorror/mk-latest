#!/usr/bin/env python3
"""PreCompact observational warn (Claude Code port of .cursor/hooks/precompact-handoff-warn.py).

Observational only — cannot block compaction. Reads Claude Code's PreCompact
payload on stdin and emits a `systemMessage` so the handoff discipline in
CLAUDE.md fires before the summary goes lossy.
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {}

    # Claude Code PreCompact fields
    trigger = data.get("trigger") or "unknown"
    custom = data.get("custom_instructions") or ""
    # Cursor-only fields — kept so the same script survives either platform
    pct = data.get("context_usage_percent")
    tokens = data.get("context_tokens")
    window = data.get("context_window_size")

    bits = [f"trigger={trigger}"]
    if pct is not None:
        bits.append(f"~{pct}%")
    if tokens is not None and window is not None:
        bits.append(f"{tokens}/{window} tok")
    if custom:
        bits.append("custom-instructions ပါ")
    meta = " · ".join(bits)

    msg = (
        f"[trc-central context] Compaction စနေပြီ ({meta}) — summary lossy ဖြစ်နိုင်။ "
        "Agent: code/Builder ရပ် · active_context.md မှာ DONE/PARTIAL/NEXT + paste ရေး · "
        "reply = handoff သာ။ User: chat အသစ်ဖွင့် · active_context paste (သို့ `handoff only` ပြော)။ "
        "ဒီ hook က warn သာ — compaction မပိတ်နိုင်။"
    )
    json.dump({"systemMessage": msg}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
