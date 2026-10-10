# GitHub — track harness files

## Goal
`.gitignore` က Cursor / Claude / SoT / CodeGraph ignore ကို ဖယ်ပြီး အဲဒီဖိုင်တွေကို GitHub `main` သို့ commit + push လုပ်မယ်။

## Core logic
1. `.gitignore` ထဲက CodeGraph၊ Cursor harness၊ Claude harness block သုံးခုကို ဖျက်
2. `.DS_Store` · `node_modules` · build output · `coverage` · `scripts/.local/` · `docs/` · `.mcp.json` ကို ignore ဆက်ထား
3. ဖိုင်တွေကို track လုပ်၊ commit၊ `gh` credential နဲ့ `origin/main` သို့ push

## Edge / Fail
- Edge: `.mcp.json` ignore ဆက်ထား — token မတက်ရ
- Fail: macOS keychain က `thihaaung225278` ဖြစ်နေလို့ plain `git push` 403။ Fallback: `gh` (`thihathehorror`) credential helper

## Status
DevOps done. Harness files committed and pushed to `origin/main`.

## Out of scope
CF3 quiz · build artifact un-ignore · `.DS_Store` · `scripts/.local/` · `.mcp.json`

```
Continue mk-latest from active_context.md + progress.md.
DONE: DevOps — harness files on origin/main
NEXT: none
SoT: active_context.md + progress.md
If context thin: handoff only — no code.
Workflow Scout→… one step per y.
```
