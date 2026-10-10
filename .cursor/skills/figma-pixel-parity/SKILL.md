---
name: figma-pixel-parity
description: 'Link-first EXACT Figma → SPFx. Use when user pastes figma.com URL with node-id (alone is enough), or PIXEL PARITY / Figma အတိုင်း / design-to-code. get_design_context first, then px-count gate: px present → sizes 1:1 into *.module.scss; px 0 (flattened vector/artwork) → get_metadata box + download_assets, never hand-written SCSS. Screenshot verifies, never measures. No Tailwind package; taste OFF. Do NOT use for classic SiteAssets PARITY or PnPjs-only.'
argument-hint: 'Figma node URL (node-id required) + target web part if known'
---

# Figma Link-First EXACT Parity (trc-central)

**အရင်လို:** Figma node link ပေးရုံ → ဒီ skill + `get_design_context`။ Magic word မလို။

Gated rule: `.cursor/rules/figma-pixel-parity.mdc`. Fast-path: `.cursorrules` `<figma_link_fast_path>`.

Also load plugin `/figma-design-to-code` before MCP calls.

## Checklist

1. **Parse** — `fileKey`, `nodeId` (`1-2` → `1:2`). No `node-id` → ask; stop.
2. **Fetch (Scout-ok)** — `get_design_context` (keep screenshot; `excludeScreenshot` မသုံးရ). Timeout → smaller child node; no freestyle.
2a. **Verify response** — `content` ထဲ `"error"` (`Not connected` / `fetch failed`) ပါရင် `isError:false` ဖြစ်လည်း **fail** → reconnect, retry. အလွတ်နဲ့ ဆက်မလုပ်ရ။
2b. **Classify (px-count gate)** — returned code ထဲ `[Npx]` တွက်:
   - **≥1 px + `<p>` text node** → live layout node → Step 3
   - **px ၀** (`inset-[…%]` သာ / `<img>` များ / `Layer_1`·`Vector`·`Group`·`Clip path group`·`clippath`·`BG_*`·`data-BG *`) → flattened vector artwork → **Step 3 skip, Step 3a သွား**
3. **Measure** *(live layout node)* — treat MCP/Tailwind reference as **rulers**: copy padding/gap/font/line-height/radius/color **numbers** into `*.module.scss`. Structure may use existing React/Fluent components; **geometry stays Figma**.
3a. **Vector path** *(px ၀)* — SCSS နဲ့ ပြန်တည်ဆောက်တာ **တားမြစ်**။ `get_metadata` → `x/y/width/height` = numeric SoT (box + placement); `download_assets` → SVG/PNG; SCSS မှာ container box + `object-fit`/`background-size` သာ ရေး။ clip-path/mask ကို hand-write **မလုပ်ရ**။
4. **Assets** — download MCP asset URLs into web part assets; wire requires. No hand-drawn SVG. Fetch fail → retry, မခန့်မှန်းရ။
5. **Architect (after Scout y)** — core logic + 1 edge + 1 fail → `active_context.md`; "Plan ဆွဲပြီးပါပြီ။ (y?)"။ **Never skip.**
6. **Build (after Architect y)** — implement web part surface only.
7. **Prove** — Figma shot vs UI shot; fix mismatches before “Figma အတိုင်း” / PASS.

## Rules of thumb

- No Tailwind/shadcn **packages**. MCP Tailwind classes are hints → SCSS values, not final classnames in SPFx.
- “Adapt to project” ≠ change layout.
- Taste heuristics OFF.
- Architect **required** on all Figma ports (`figma_link_fast_path` = Scout `get_design_context` gather only — not Architect skip).

## Reject

- Screenshot-only coding
- **SCSS ရေးတာ — `get_design_context` က px ၀ ပြန်ထားပြီးမှ** (= ပုံကြည့် ခန့်မှန်းတာ)
- **flattened vector / clip-path / mask ကို hand-written SCSS နဲ့ ပြန်တည်ဆောက်**
- `{"error": …}` + `isError:false` ကို success လို့ သတ်မှတ်
- parity task မှာ `excludeScreenshot` ပါ
- Close enough / redesign
- PASS without evidence
