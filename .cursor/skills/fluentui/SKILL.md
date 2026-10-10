---
name: fluentui
description: 'Fluent UI React v8 consumer for SPFx 1.23. Use when: @fluentui/react, ThemeProvider, createTheme, initializeIcons, Stack, Panel, Button, Dialog, theme palette, hardcoded hex → palette, CMS toolbar/property-pane React UI. v9 refs for migration planning only. Do NOT use for game canvas, vanilla JS, or ASPX-only CSS.'
argument-hint: 'Describe the Fluent UI task: component, theme, icons, or SPFx web part UI'
---

# Fluent UI (Consumer · SPFx · v8)

Adapted from [microsoft/fluentui](https://github.com/microsoft/fluentui) `AGENTS.md` and `token-lookup` skill — **consumer slice only** (not monorepo contributor).

## This repo (verify `package.json`)

| Package | Version lane | Use |
| --- | --- | --- |
| `@fluentui/react` | **v8** (SPFx 1.23) | Primary — Stack, Text, Button, Panel, Dialog, theme, icons |
| `@fluentui/react-components` | v9 (not installed) | Future migration — `references/v9-rules.md` |
| `@fluentui/react-icons` | v9 (not installed) | Future migration |

MUST verify versions against `package.json`. Do not invent packages this repo does not declare.

## Route by intent (load ONE reference)

| Intent | Read |
| --- | --- |
| v8 rules, anti-patterns, what not to copy | [v8-rules.md](./references/v8-rules.md) |
| Theme, palette, `createTheme`, `ThemeProvider` | [v8-theme.md](./references/v8-theme.md) |
| Components — Stack, Panel, Button, overlays | [v8-components.md](./references/v8-components.md) |
| Icons — `initializeIcons`, property pane | [v8-icons.md](./references/v8-icons.md) |
| Hex / CSS value → palette key | [token-lookup-v8.md](./references/token-lookup-v8.md) — optional: `python scripts/token-lookup.py '#0078d4'` |
| v9 migration / Griffel / react-components | [v9-rules.md](./references/v9-rules.md), [tokens.md](./references/tokens.md) |
| SPFx host layout + web part UI contract | [../spfx/references/react-design.md](../spfx/references/react-design.md) |
| SPFx create / upgrade / PnPjs / Heft | [../spfx/SKILL.md](../spfx/SKILL.md) |

## Quick rules (v8 SPFx)

1. Fluent primitives (`Stack`, `Text`, `PrimaryButton`, `Panel`, …) before raw HTML where the web part already uses Fluent.
2. Theme via `ThemeProvider` + `createTheme` / `getTheme` — match SharePoint host; no random brand hex in new UI.
3. SCSS modules for layout; Fluent for interactive controls and typography scale.
4. Property-pane / portal overlays: respect `PROPERTY_PANE_MODAL_Z_INDEX` pattern in this repo.
5. Prefer project `.cursor/skills/fluentui` over any global copy.

## When NOT to load this skill

- Game canvas controllers (`*Game.ts`, `GameController.ts`) — CSS/SCSS only
- Vanilla JS / ASPX markup without React Fluent surfaces
- PnPjs / list CRUD with no UI component work
- SPFx scaffold / upgrade with no Fluent component task

## Upstream reject list

Do **not** route to microsoft/fluentui monorepo contributor skills: `v9-component`, `headless-component`, `change` (beachball), `lint-check`, `package-info`, `review-pr`, `triage-issues`, `dependabot-rollup`, `visual-test`.

## Guards

- Do not npm-install v9 packages into SPFx 1.23 without explicit upgrade/migration task.
- Do not copy legacy v8 monorepo internals — follow consumer refs above.
