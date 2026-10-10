# SPFx Toolchain — Heft vs gulp

Determine the installed SPFx version before running any build command.

## Version detect

1. Read `.yo-rc.json` → `@microsoft/generator-sharepoint.version`
2. Or read `package.json` → `@microsoft/sp-*` package versions
3. Check `useGulp` in `.yo-rc.json` — `false` means Heft (v1.22+)

| Installed SPFx version | Toolchain |
| --- | --- |
| **v1.22.0 and newer** | **Heft** |
| **v1.0 – v1.21.1** | **gulp** (legacy) |

**This repo:** SPFx **1.23.0** · Heft · Node `>=22.14.0 < 23.0.0`

## Heft commands (v1.22+ · this repo)

### Local development (serve + workbench)

```bash
npm start
# or targeted serve config:
npm run start:page
npm run start:wp -- <WebPartName>
```

Underlying: `heft start --clean --serve-config <name>`

### Build

```bash
npm run build:fast    # heft build --production (no package)
npm run build         # full production build + package-solution
npm test              # heft test --clean --production
npm run clean         # remove lib/dist/temp/sharepoint artifacts
```

### Package for deployment

```bash
npm run build:package   # prepare assets + heft package-solution --production
```

Output: `sharepoint/solution/*.sppkg`

### Verify (this repo scripts)

```bash
npm run verify:package
npm run verify:manifests
npm run verify:sppkg
```

## Legacy gulp commands (≤ v1.21.1 only)

Do **not** use these in this repo unless upgrading down-level solutions.

```bash
gulp serve
gulp bundle --ship
gulp package-solution --ship
```

## gulp → Heft migration

When upgrading a legacy project to v1.22+:

1. Follow [upgrade.md](./upgrade.md) via `m365 spfx project upgrade`
2. Apply all report steps in order
3. Replace `gulp serve` → `heft start` / `npm start`
4. Replace `gulp bundle --ship` → `heft build --production`
5. Replace `gulp package-solution --ship` → `heft package-solution --production`
6. Run `npm run build` until clean

## Validation rule

After toolchain or build-config changes:

1. Run `npm run build` (or `npm run build:fast` for code-only changes)
2. Resolve every error — task is not done until build is clean
3. Smoke-test: `npm start` → workbench → target web part
4. Tell user to review git diff before committing

## npm install note

SPFx dependency trees are heavy. When running `npm install`, use synchronous execution with a timeout of at least **3 minutes**:

```bash
npm install --silent --no-fund --no-audit
```
