#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

API_DIR="apps/api"
API_VENV="$API_DIR/.venv"
API_HOST="0.0.0.0"
API_PORT="8000"
WEB_PORT="3000"

ensure_postgres() {
  if nc -z localhost 5432 2>/dev/null; then
    echo "✓ Postgres is already running on :5432"
    return 0
  fi
  echo "→ Starting Postgres..."
  if command -v pg_ctlcluster >/dev/null 2>&1; then
    sudo -n pg_ctlcluster 17 main start 2>/dev/null || pg_ctlcluster 17 main start 2>/dev/null || true
  elif command -v service >/dev/null 2>&1; then
    sudo -n service postgresql start 2>/dev/null || service postgresql start 2>/dev/null || true
  elif command -v brew >/dev/null 2>&1; then
    brew services start postgresql@17 2>/dev/null || brew services start postgresql 2>/dev/null || true
  fi
  sleep 2
  if nc -z localhost 5432 2>/dev/null; then
    echo "✓ Postgres started on :5432"
  else
    echo "⚠ Postgres not running on :5432 — start it manually or use Docker (scripts/dev.sh)"
  fi
}

ensure_api_venv() {
  if [ ! -d "$API_VENV" ]; then
    echo "→ Creating API virtualenv..."
    python3 -m venv "$API_VENV"
  fi
  echo "→ Installing API dependencies..."
  "$API_VENV/bin/pip" install -e "$API_DIR[dev]"
}

start_api() {
  echo "→ Starting API (uvicorn --reload) on http://$API_HOST:$API_PORT"
  cd "$API_DIR"
  source .venv/bin/activate
  uvicorn app.main:app --host "$API_HOST" --port "$API_PORT" --reload &
  API_PID=$!
  cd - >/dev/null
}

start_web() {
  echo "→ Starting web (next dev) on http://localhost:$WEB_PORT"
  pnpm --filter @openschoolos/web dev --port "$WEB_PORT" --hostname "0.0.0.0" &
  WEB_PID=$!
}

cleanup() {
  echo ""
  echo "→ Stopping services..."
  [ -n "${WEB_PID:-}" ] && kill "$WEB_PID" 2>/dev/null || true
  [ -n "${API_PID:-}" ] && kill "$API_PID" 2>/dev/null || true
  wait 2>/dev/null || true
  echo "✓ Stopped."
}

trap cleanup EXIT

ensure_postgres
ensure_api_venv
start_api
sleep 2
start_web

echo ""
echo "✓ OpenSchoolOS is running:"
echo "  • Web:  http://localhost:$WEB_PORT"
echo "  • API:  http://$API_HOST:$API_PORT"
echo "  • Docs: http://$API_HOST:$API_PORT/docs"
echo ""
echo "Press Ctrl+C to stop."
wait
