---
name: spfx
description: 'SharePoint Framework (SPFx) development. Use when: "create SPFx project", "new web part", "SPFx extension", "upgrade SPFx", "SPFx upgrade", "update SPFx version", "scaffold SPFx", "SPFx React", "SPFx design", "web part styling", "Fluent UI in SPFx", "SPFx Heft", "gulp to Heft", "PnPjs", "read SharePoint list", "call Microsoft Graph from SPFx". Covers project creation (Yeoman), upgrades (CLI for Microsoft 365), the Heft/gulp toolchain, React web part design, and PnPjs data access.'
argument-hint: 'Describe what you need: create, upgrade, design, or data access'
---

# SPFx Development

> **Upstream:** adapted from [SharePoint/spfx-dev-skills](https://github.com/SharePoint/spfx-dev-skills) (MIT) — consumer slice for this repo.
> **This repo:** SPFx **1.23** · **Heft** · `@fluentui/react` **v8** · PnPjs default for data.

Pick the reference(s) that match the user's intent. Load **only** what is needed and execute the steps exactly:

| Intent | Reference |
| --- | --- |
| **Create** a project / web part / extension | [create.md](./references/create.md) |
| **Upgrade** SPFx version / gulp→Heft | [upgrade.md](./references/upgrade.md) |
| **SharePoint / Graph data** (lists, items, files) | [pnpjs.md](./references/pnpjs.md) |
| **Build / serve / package** (Heft or gulp) | [toolchain.md](./references/toolchain.md) |
| **Web part UI shell** (layout, a11y, host awareness) | [react-design.md](./references/react-design.md) |

## Routing split (do not double-load)

- **Fluent components / theme / icons / palette / visual design** → `.cursor/skills/fluentui/SKILL.md` via `fluentui-gated.mdc` — not this skill
- **This skill** → scaffold, upgrade, data, toolchain, web-part shell contract only

## Global rules (apply to every SPFx task)

- **Use PnPjs by default** for all SharePoint and Microsoft Graph data operations. See [pnpjs.md](./references/pnpjs.md). Only fall back to raw `SPHttpClient`/`MSGraphClientV3` when the user explicitly requires it or a dependency cannot be added.
- **When running `npm install`, always run it synchronously with a timeout of at least 3 minutes.** SPFx projects have heavy dependency trees.
- **Never scaffold** into game canvas, vanilla JS controllers, or ASPX-only markup.
- **Validate with a clean build** before calling a task done — see [toolchain.md](./references/toolchain.md).

## Toolchain decision rule

SPFx switched build systems at v1.22.0. Determine the version from `.yo-rc.json` (`@microsoft/generator-sharepoint.version`) or `package.json`, then:

| Installed SPFx version | Toolchain | Reference |
| --- | --- | --- |
| **v1.22.0 and newer** | **Heft** | [toolchain.md](./references/toolchain.md) |
| **v1.0 – v1.21.1** | **gulp** (legacy) | [toolchain.md](./references/toolchain.md) |
