#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/platform/backend"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  .venv/bin/python -m ensurepip --upgrade 2>/dev/null || true
fi

. .venv/bin/activate
python -m pip install -q -r requirements.txt

if [ -f "$ROOT/platform/.env" ]; then
  export $(grep -v '^#' "$ROOT/platform/.env" | xargs)
fi

echo "Manimations Studio API → http://127.0.0.1:8000"
echo "Data dir: ~/manimations-studio"
exec python run.py
