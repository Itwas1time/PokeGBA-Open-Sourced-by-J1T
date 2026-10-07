#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "${POKEMON_GBA_PYTHON:-python3}" "$SCRIPT_DIR/pokemon-gba-menu.py"
