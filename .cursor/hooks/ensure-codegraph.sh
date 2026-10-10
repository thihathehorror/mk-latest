#!/usr/bin/env bash
# Auto-initialize CodeGraph when a session starts and no local index exists.
set -euo pipefail

ROOT="${CURSOR_PROJECT_DIR:-$(pwd)}"
DB="${ROOT}/.codegraph/codegraph.db"

if [[ -f "$DB" ]]; then
  exit 0
fi

if ! command -v codegraph >/dev/null 2>&1; then
  exit 0
fi

codegraph init "$ROOT" >/dev/null 2>&1 || true
exit 0
