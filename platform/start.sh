#!/usr/bin/env bash
# Start both backend and frontend (run in two terminals for cleaner logs, or use this)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Starting Manimations Studio..."
echo "  Backend:  http://127.0.0.1:8000"
echo "  Frontend: http://127.0.0.1:5173"
echo ""
echo "Set OPENAI_API_KEY in platform/.env before chatting."
echo ""

chmod +x "$ROOT/platform/start-backend.sh" "$ROOT/platform/start-frontend.sh"

# Start backend in background
"$ROOT/platform/start-backend.sh" &
BACKEND_PID=$!

trap "kill $BACKEND_PID 2>/dev/null" EXIT

sleep 2
"$ROOT/platform/start-frontend.sh"
