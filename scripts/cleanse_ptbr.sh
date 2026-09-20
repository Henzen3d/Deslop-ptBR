#!/usr/bin/env bash
# Deslop PT-BR Cleanse Shell Wrapper
# Executa a limpeza com modelo rival delegando para o scripts/cleanse_ptbr.py
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    PYTHON_BIN="python"
fi

exec "$PYTHON_BIN" "$HERE/cleanse_ptbr.py" "$@"
