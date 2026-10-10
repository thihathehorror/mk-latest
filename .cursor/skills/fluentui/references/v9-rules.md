# Fluent UI v9 consumer rules

Adapted from [microsoft/fluentui AGENTS.md](https://github.com/microsoft/fluentui/blob/master/AGENTS.md) for **app consumers** (not monorepo contributors).

## Critical

1. **No hardcoded visual values** in React UI — use `tokens` from `@fluentui/react-theme` (see [tokens.md](./tokens.md)).
2. **New UI = v9 only** — `@fluentui/react-components` + `@fluentui/react-icons`. Do not start new work on `@fluentui/react` (v8) or `mergeStyles` / `initializeIcons()`.
3. **FluentProvider** — wrap themed surfaces; inherit host/SharePoint theme when in SPFx (see `spfx/references/react-design.md`).
4. **Compose, don't reinvent** — use Fluent primitives (Button, Input, Dialog, …) before custom HTML/CSS components.
5. **Verify before import** — match package versions to the target project's `package.json` / SPFx stack. If undeclared, say so; do not invent installs unless the user asks.

## Styling

- Prefer Griffel `makeStyles` + tokens when the project already uses Griffel/Fluent v9.
- `mergeClasses`: keep user `className` **last**.
- Do not use v8 `mergeStyles` / `IStyle` / `IStyleFunctionOrObject` for new code.

## Icons

- Use `@fluentui/react-icons` (tree-shakeable). Do not call `initializeIcons()`.

## Classic ASPX (this repo)

- These rules apply when generating **React/SPFx** Fluent UI.
- Classic `.aspx` pages: do not bundle React+Fluent unless the user explicitly requests SPFx (or React) scaffolding.

## Out of scope here

Monorepo-only workflows — Nx generators, beachball change files, Fluent UI issue triage, Dependabot rollup — are not part of this skill.
