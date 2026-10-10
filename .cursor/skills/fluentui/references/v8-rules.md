# Fluent UI v8 consumer rules (SPFx 1.23)

Adapted from [microsoft/fluentui AGENTS.md](https://github.com/microsoft/fluentui/blob/master/AGENTS.md) for **app consumers** — not monorepo contributors.

## Critical (this repo)

1. **No hardcoded palette in new Fluent React UI** — use `ITheme.palette` via `createTheme`, `getTheme()`, or `theme` prop on styled components. See [v8-theme.md](./v8-theme.md).
2. **Package = `@fluentui/react` v8 only** — verify `package.json`. Do not import `@fluentui/react-components` or `@fluentui/react-icons` unless migration task explicitly adds them.
3. **Compose from Fluent primitives** — `Stack`, `Text`, `PrimaryButton`, `DefaultButton`, `Panel`, `Dialog`, `Dropdown`, `Icon` before custom HTML/CSS controls.
4. **Verify before import** — match API to installed v8; do not invent props or packages.
5. **SPFx React 17** — use existing `ReactDom.render` / `React.createElement` patterns in property-pane hosts; do not assume React 18 APIs.

## Styling

- Prefer component `styles` / `style` props and `IStackStyles`, `ITextStyles`, etc.
- `mergeStyles` / `mergeStyleSets` — only when surrounding code already uses them; do not introduce for new simple UI.
- SCSS modules (`.module.scss`) for layout shells; Fluent for interactive controls.
- SharePoint CSS variables (`var(--themePrimary)`) acceptable in injected runtime CSS that must match host chrome — see `src/shared/canvasFullBleedSelectors.ts`.

## Icons

- v8: `initializeIcons` once per host — see [v8-icons.md](./v8-icons.md).
- Do not call `initializeIcons` in every component render.

## Legacy anti-patterns (do not copy into new code)

- Do not start new features on v9 APIs while v8 is the declared stack.
- Do not recreate Fluent button/panel anatomy with raw `<button>` + custom CSS when Fluent components exist in the same surface.
- Do not use `React.FC` as a hard requirement — match existing file style in the web part being edited.

## Classic ASPX / game surfaces

- Rules apply to **SPFx React TSX** (property pane, CMS toolbars, media pickers).
- Game canvas / vanilla TS — CSS/SCSS only unless user explicitly migrates that surface to React.

## Out of scope

Monorepo workflows — Nx, beachball, v9 component scaffolding, issue triage — see SKILL.md reject list.
