# Fluent UI v8 icons (SPFx)

Package: `@fluentui/react` v8 — icons via `initializeIcons` + `Icon` / `IconButton`.

## One-time registration (this repo)

```ts
import { initializeIcons } from '@fluentui/react/lib/Icons';

let ready = false;

export function ensureFluentPropertyPane(): void {
  if (ready || typeof window === 'undefined') {
    return;
  }
  initializeIcons(undefined, { disableWarnings: true });
  ready = true;
}
```

Reference: `src/webparts/techRiskCulture/propertyPane/initializeFluentPropertyPane.ts`.

Call `ensureFluentPropertyPane()` before `ReactDom.render` in property-pane hosts and game CMS toolbars that use Fluent icons.

## Using icons in JSX

```tsx
import { Icon, IconButton } from '@fluentui/react';

<Icon iconName="Photo2" aria-hidden />
<IconButton iconProps={{ iconName: 'Cancel' }} ariaLabel="Close" onClick={onClose} />
```

- Decorative icons: `aria-hidden`
- Interactive: `IconButton` with `ariaLabel` (not icon-only without label)

## Game-specific icon modules

Some web parts isolate icon setup:

- `src/webparts/whatsTheRightMove/game/wtrmFluentIcons.ts`
- `src/webparts/raiseTheAlarm/game/raiseTheAlarmFluentIcons.ts`

Follow the same idempotent `initializeIcons` pattern; do not register on every frame.

## v9 migration note

`@fluentui/react-icons` (tree-shakeable) is **not** installed. Do not use v9 icon imports until migration task adds the package. See [v9-rules.md](./v9-rules.md).
