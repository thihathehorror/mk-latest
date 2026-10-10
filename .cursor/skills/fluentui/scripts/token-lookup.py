#!/usr/bin/env python3
"""Map hardcoded CSS colors to Fluent UI v8 ITheme.palette keys (consumer helper)."""

from __future__ import annotations

import re
import sys

# Common Fluent / SharePoint default palette (v8 consumer subset)
PALETTE: dict[str, str] = {
    "themePrimary": "#0078d4",
    "themeDarkAlt": "#106ebe",
    "themeDark": "#005a9e",
    "themeDarker": "#004578",
    "themeLight": "#c7e0f4",
    "themeLighter": "#deecf9",
    "themeLighterAlt": "#eff6fc",
    "neutralPrimary": "#323130",
    "neutralSecondary": "#605e5c",
    "neutralTertiary": "#a19f9d",
    "neutralQuaternary": "#8a8886",
    "neutralLight": "#edebe9",
    "neutralLighter": "#f3f2f1",
    "neutralLighterAlt": "#faf9f8",
    "white": "#ffffff",
    "black": "#000000",
    "redDark": "#a4262c",
    "green": "#107c10",
    "yellow": "#ffb900",
    "orange": "#d83b01",
}

REVERSE = {v.lower(): k for k, v in PALETTE.items()}


def normalize_hex(value: str) -> str | None:
    value = value.strip().lower()
    if value in REVERSE:
        return value
    m = re.match(r"^#([0-9a-f]{3}|[0-9a-f]{6})$", value)
    if not m:
        return None
    hex_part = m.group(1)
    if len(hex_part) == 3:
        hex_part = "".join(c * 2 for c in hex_part)
    return f"#{hex_part}"


def hex_distance(a: str, b: str) -> int:
    ar, ag, ab = int(a[1:3], 16), int(a[3:5], 16), int(a[5:7], 16)
    br, bg, bb = int(b[1:3], 16), int(b[3:5], 16), int(b[5:7], 16)
    return (ar - br) ** 2 + (ag - bg) ** 2 + (ab - bb) ** 2


def lookup(query: str) -> str:
    q = query.strip()
    if q in PALETTE:
        return f"palette.{q} = {PALETTE[q]}"

    normalized = normalize_hex(q)
    if normalized is None:
        return f"Unknown value: {q!r}. Use a #hex color or palette key name."

    if normalized in REVERSE:
        key = REVERSE[normalized]
        return (
            f"// Instead of: {normalized}\n"
            f"theme.palette.{key}  // {PALETTE[key]}"
        )

    closest = min(PALETTE.items(), key=lambda item: hex_distance(normalized, item[1]))
    key, hex_val = closest
    return (
        f"// No exact match for {normalized}\n"
        f"// Closest: theme.palette.{key}  // {hex_val}\n"
        f"// Verify visually before replacing."
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: token-lookup.py <#hex|paletteKey>", file=sys.stderr)
        print("Example: token-lookup.py '#0078d4'", file=sys.stderr)
        return 1
    print(lookup(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
