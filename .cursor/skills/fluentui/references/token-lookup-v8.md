# Design token lookup — Fluent UI v8 (`ITheme.palette`)

Find the correct **palette** or **semantic** key for a hardcoded CSS value in v8 SPFx UI.

Adapted from [microsoft/fluentui token-lookup skill](https://github.com/microsoft/fluentui/tree/master/.agents/skills/token-lookup) for `@fluentui/react` v8 consumers.

## Steps

1. **Categorize the value** — color → `palette.*`; spacing often → `spacing` on `Stack` tokens or SCSS; font → `fonts` / `Text` variant.
2. **Search this table** (common SharePoint / Fluent defaults).
3. **Use in theme or styles:**

```tsx
import { createTheme, getTheme } from '@fluentui/react';

const theme = getTheme();
// Instead of: color: '#0078d4'
color: theme.palette.themePrimary;
```

4. **CLI (optional):**

```bash
python .cursor/skills/fluentui/scripts/token-lookup.py '#323130'
python .cursor/skills/fluentui/scripts/token-lookup.py themePrimary
```

5. **No exact match** — pick closest semantic palette key; note delta in PR comment.

## Common color mappings

| Hardcoded | Palette key |
| --- | --- |
| `#0078d4` | `themePrimary` |
| `#106ebe` | `themeDarkAlt` |
| `#005a9e` | `themeDark` |
| `#c7e0f4` | `themeLight` |
| `#deecf9` | `themeLighter` |
| `#eff6fc` | `themeLighterAlt` |
| `#323130` | `neutralPrimary` |
| `#605e5c` | `neutralSecondary` |
| `#a19f9d` | `neutralTertiary` |
| `#f3f2f1` | `neutralLighter` |
| `#edebe9` | `neutralLight` |
| `#ffffff` | `white` |
| `#a4262c` | `redDark` (error text) |
| `#107c10` | `green` (success) |

## Stack spacing (not palette)

| Hardcoded gap | Prefer |
| --- | --- |
| `4px` | `tokens={{ childrenGap: 4 }}` on `Stack` |
| `8px` | `childrenGap: 8` |
| `16px` | `childrenGap: 16` |

## v9 tokens

For `@fluentui/react-theme` / Griffel `tokens.*` — project does not install v9; see [tokens.md](./tokens.md) for migration reference only.

## Fallback

If `token-lookup.py` fails, use this table manually — script is optional.
