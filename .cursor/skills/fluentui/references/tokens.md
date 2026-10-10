# Fluent UI design tokens (consumer)

Never hardcode colors, spacing, typography, radius, or shadows in Fluent React UI. Use tokens from `@fluentui/react-theme`.

```tsx
import { tokens } from '@fluentui/react-theme';
import { makeStyles } from '@griffel/react';

export const useStyles = makeStyles({
  root: {
    color: tokens.colorNeutralForeground1,
    backgroundColor: tokens.colorNeutralBackground1,
    padding: `${tokens.spacingVerticalS} ${tokens.spacingHorizontalM}`,
    borderRadius: tokens.borderRadiusMedium,
    fontSize: tokens.fontSizeBase300,
    fontWeight: tokens.fontWeightSemibold,
    boxShadow: tokens.shadow4,
  },
});
```

## Common mappings (verify against installed theme)

| Hardcoded | Token |
| --- | --- |
| `#0078d4` | `tokens.colorBrandBackground` |
| `#323130` | `tokens.colorNeutralForeground1` |
| `#ffffff` | `tokens.colorNeutralBackground1` |
| `4px` radius | `tokens.borderRadiusMedium` |
| `8px` padding | `tokens.spacingHorizontalS` / `tokens.spacingVerticalS` |
| `14px` font | `tokens.fontSizeBase300` |
| `600` weight | `tokens.fontWeightSemibold` |

No exact match → pick the closest **semantic** token and note the difference. Prefer brand/neutral/status semantics over raw palette hex.

## Categories

| Value looks like | Token family |
| --- | --- |
| hex / rgb / named color | `color*` |
| px/rem spacing | `spacingHorizontal*` / `spacingVertical*` |
| font size | `fontSize*` |
| font weight | `fontWeight*` |
| border radius | `borderRadius*` |
| shadow | `shadow*` |
| border width | `strokeWidth*` |
| duration | `duration*` |

## Docs

- Consumer Storybook: https://react.fluentui.dev/
- Upstream token concepts: https://github.com/microsoft/fluentui (design-tokens architecture under `docs/`)
