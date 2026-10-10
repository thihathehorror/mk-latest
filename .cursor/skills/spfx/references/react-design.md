# React SPFx Design Guidelines — Copilot UI Contract v2.1

> **THIS REPO = Fluent UI v8** (`@fluentui/react` ^8.x, SPFx 1.23). Use `ThemeProvider` + `createTheme` — not v9 `FluentProvider` / `@fluentui/react-components` unless a migration task adds those packages.

(Fluent UI v8 + SharePoint + Host Awareness)

Normative guidance for generating UI consistent with Fluent UI **v8**, aligned to SharePoint experiences, and adaptable across host environments.

## 1. Scope

Applies to UI generated as:

- primitive (button, input, badge)
- composite (toolbar, card, feed item)
- assembly (feed, dashboard section, form)
- template (full page or multi-region flow)

Agents MUST NOT assume all requests are full-page experiences.

## 2. Platform

Generated UI MUST use:

- React
- TypeScript
- SPFx-compatible patterns
- **@fluentui/react** (v8)
- **initializeIcons** (v8) where icons are used — see `.cursor/skills/fluentui/references/v8-icons.md`

Agents MUST NOT recreate Fluent components using custom HTML/CSS.

MUST verify the Fluent UI version against the project's `package.json` before importing. Match the version aligned to the installed SPFx; do not assume a version the project does not declare.

**Future migration:** v9 (`@fluentui/react-components`, `@fluentui/react-icons`) — planning only; see `.cursor/skills/fluentui/references/v9-rules.md`.

## 3. Core Rules

- MUST use Fluent UI v8 components when available
- MUST compose from Fluent primitives before custom UI
- MUST produce accessible, responsive output
- SHOULD keep output minimal and implementation-ready
- MAY add small custom styling when required

## 4. Theme and Host Precedence

Apply in order:

1. Accessibility and legibility
2. Host surface integration
3. SharePoint alignment
4. Brand expression via palette / theme

- MUST inherit theme, colors, typography from host
- MUST NOT hardcode colors or surfaces in new Fluent React UI
- SHOULD use neutral, adaptive surfaces

## 5. Theme Application

Generated UI MUST demonstrate theme integration.

- MUST use **ThemeProvider** (v8) when theming is relevant
- MUST use **ITheme.palette** keys (no fixed colors in new code)
- SHOULD accept theme via `createTheme` or context
- MUST fallback to Fluent defaults when no host theme exists

See `.cursor/skills/fluentui/references/v8-theme.md`.

## 6. SharePoint Alignment

- MUST respect SharePoint themes when present
- MUST adapt to zones, columns, dynamic width
- SHOULD use patterns: cards, lists, panels, sections
- MUST NOT assume app-shell layout unless specified

## 7. Container Context Rules

Agents MUST infer context.

### Inline / Conversational

- MUST use single-column layout
- MUST prioritize scannability
- MUST NOT rely on hover-only interactions
- SHOULD avoid dense toolbars/forms

### Embedded / Web Part

- MUST assume constrained width
- MUST use compact density
- MUST minimize padding and elevation
- SHOULD favor vertical layouts
- MUST resize cleanly across zones

### Full Page

- MAY use multi-column layouts
- MAY introduce stronger hierarchy

## 8. Component Composition Rules

- MUST use Fluent subcomponents and variants (`Text` variants, `Panel` footer, etc.)
- MUST NOT recreate component anatomy manually
- MUST use proper Text hierarchy (size/weight)
- MUST avoid arbitrary spacing — prefer `Stack` `tokens.childrenGap`

## 9. Interaction Consistency

- MUST use consistent interaction states (hover/active/focus)
- SHOULD use MDL2 icon names consistently via `Icon` / `IconButton`
- MUST NOT mix inconsistent icon styles

## 10. Accessibility

- MUST use semantic structure
- MUST support keyboard navigation
- MUST include labels/accessible names
- MUST preserve tab order
- MUST manage focus for overlays
- MUST expose loading/empty/error states

## 11. Performance

- SHOULD favor lightweight composition
- SHOULD avoid excessive nesting
- SHOULD avoid heavy components unless justified

## 12. Styling

- MUST prefer Fluent defaults
- MUST NOT assume fixed widths
- MUST maintain readability in narrow views
- SHOULD use `ITheme.palette` and Stack tokens

## 13. Anti-Patterns

Agents MUST NOT:

- recreate Fluent components manually
- assume full-screen layouts in embedded contexts
- use custom color systems
- overuse elevation
- create dense multi-column layouts in narrow spaces
- rely on hover-only affordances
- import v9 packages in this repo without explicit migration scope

## 14. Output

Generated output MUST be:

- React + TypeScript
- Fluent UI **v8**-based
- readable and implementation-ready

## 15. Data Access

- MUST use **PnPjs by default** for any SharePoint or Microsoft Graph data — see [pnpjs.md](./pnpjs.md).
- MUST keep data calls in a service or hook, never inside render.
- MUST expose loading, empty, and error states for all async data.

## 16. Validation

After UI changes, MUST run `npm run build` and resolve all errors, then smoke-test in the workbench (`heft start` on SPFx v1.22+, `gulp serve` on legacy — see [toolchain.md](./toolchain.md)).
