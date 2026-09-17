#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
trap 'kill 0' EXIT
(cd "$ROOT/backend" && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000) &
(cd "$ROOT/frontend" && npm run dev -- --port 5173) &
wait
