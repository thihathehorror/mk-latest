# Fluent UI v8 components (SPFx patterns)

Package: `@fluentui/react` v8. Verify imports against existing web part files before adding new ones.

## Layout — Stack

```tsx
import { Stack } from '@fluentui/react';

<Stack tokens={{ childrenGap: 8 }} wrap>
  <PrimaryButton text="Save" onClick={onSave} />
  <DefaultButton text="Cancel" onClick={onCancel} />
</Stack>
```

- Use `tokens.childrenGap` instead of arbitrary margin between Fluent children.
- `horizontal` + `wrap` for toolbars and footer rows (see `SiteAssetMediaPickerDialog.tsx`).

## Panel (modal side sheet)

```tsx
import { Panel, PanelType, PrimaryButton, DefaultButton, Stack } from '@fluentui/react';

<Panel
  isOpen
  type={PanelType.medium}
  headerText="Select image"
  onDismiss={onClose}
  isLightDismiss
  closeButtonAriaLabel="Close"
  layerProps={{ styles: { root: { zIndex: PROPERTY_PANE_MODAL_Z_INDEX } } }}
  onRenderFooterContent={() => (
    <Stack horizontal tokens={{ childrenGap: 8 }} wrap>
      <PrimaryButton text="Insert" onClick={commit} />
      <DefaultButton text="Cancel" onClick={onClose} />
    </Stack>
  )}
  isFooterAtBottom
>
  {children}
</Panel>
```

- Import `PROPERTY_PANE_MODAL_Z_INDEX` from property-pane modal helper when stacking above SharePoint property pane.
- Always set `closeButtonAriaLabel` and meaningful `headerText`.

## Buttons

| Component | Use |
| --- | --- |
| `PrimaryButton` | Primary action (save, insert, publish) |
| `DefaultButton` | Secondary (cancel, back) |
| `IconButton` | Icon-only (close, preview) — require `ariaLabel` |

## Text hierarchy

```tsx
import { Text } from '@fluentui/react';

<Text variant="mediumPlus">Section title</Text>
<Text variant="small" styles={{ root: { color: palette.neutralSecondary } }}>Hint</Text>
```

Prefer `variant` over manual font-size when possible.

## Dropdown / Separator (CMS toolbars)

See `GoodCatchCmsPreviewToolbar.tsx` — `Dropdown` with `IDropdownStyles`, `Separator` with `ISeparatorStyles`, chrome `Stack` with dashed border for edit-mode affordance.

## Styled partials

Use `Partial<IStackStyles>`, `ITextStyles`, etc. at module scope when styles are static; keep theme colors on `palette` keys from `createTheme`.

## Anti-patterns

- Raw `<button>` next to Fluent buttons in the same toolbar
- Fixed pixel widths on panels without narrow-zone testing
- Missing z-index on overlays inside property pane (buried under SharePoint UI)
- Hardcoded error red (`#a4262c`) — prefer `palette.redDark` or semantic error styling when touching that line

## After changes

Run `npm run build` and smoke-test in workbench (`heft start`).
