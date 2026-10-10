# Fluent UI v8 theming (SPFx)

## Stack

- Package: `@fluentui/react` v8
- APIs: `createTheme`, `ThemeProvider`, `getTheme`, `loadTheme` (global), `ITheme`, `IPalette`

## Pattern in this repo

Property-pane and authoring hosts wrap React trees with `ThemeProvider`:

```tsx
import { ThemeProvider, createTheme } from '@fluentui/react';

const spTheme = createTheme({
  defaultFontStyle: {
    fontFamily: '"Segoe UI", "Segoe UI Web (West European)", -apple-system, BlinkMacSystemFont, sans-serif'
  }
});

// ReactDom.render(
//   <ThemeProvider theme={spTheme}>...</ThemeProvider>,
//   host
// );
```

References: `src/webparts/techRiskCulture/edit/cardListEditHost.ts`, `propertyPane/mediaPicker/renderSiteAssetMediaPickerField.ts`.

## Authoring chrome (CMS preview toolbars)

When Fluent UI must match SharePoint + brand on edit surfaces, extend `palette` and `effects` in `createTheme` — mirror `GoodCatchCmsPreviewToolbar.tsx` / `WtrmCmsPreviewToolbar.tsx`:

| Palette key | Typical use |
| --- | --- |
| `themePrimary` | Brand actions, accents |
| `themeDark` / `themeLight` | Hover / subtle fills |
| `neutralPrimary` | Body text |
| `neutralSecondary` | Secondary labels |
| `neutralLighter` / `neutralLight` | Surfaces |
| `white` | Cards on tinted backgrounds |

Prefer palette keys over repeating hex in `IStackStyles` / `ITextStyles`.

## Reading theme in components

```tsx
import { getTheme } from '@fluentui/react';

const theme = getTheme();
const brand = theme.palette.themePrimary;
```

Use when a component needs dynamic color but is already under `ThemeProvider`.

## SharePoint host alignment

1. Inherit Segoe / host font via `defaultFontStyle` when rendering inside SPFx chrome.
2. Do not fight SharePoint theme with unrelated color systems on authoring toolbars.
3. Injected page CSS that restores SharePoint command bar may use `var(--themePrimary, #0078d4)` — scoped runtime overrides only.

## Hardcoded value → palette

Run [token-lookup-v8.md](./token-lookup-v8.md) or:

```bash
python .cursor/skills/fluentui/scripts/token-lookup.py '#0078d4'
```

## v9 note

`FluentProvider` + `@fluentui/react-theme` tokens are **not** installed in this repo. Migration planning → [v9-rules.md](./v9-rules.md).
