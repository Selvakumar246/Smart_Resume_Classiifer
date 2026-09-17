#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/backend"
[ -f .env ] || cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cd "$ROOT/frontend"
[ -f .env ] || cp .env.example .env
npm install
printf '\nSetup complete. Run ./run-unix.sh\n'
