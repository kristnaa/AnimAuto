#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/platform/frontend"

if [ ! -d node_modules ]; then
  npm install
fi

echo "Manimations Studio UI → http://127.0.0.1:5173"
exec npm run dev
