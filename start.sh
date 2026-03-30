#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
HOST="127.0.0.1"
PORT="8001"
CONFIG_PATH="config/source-repos.json"
OUTPUT_DIR=".generated"
SOURCE_MODE="${DOCS_SOURCE_MODE:-local}"
export UV_CACHE_DIR="$PROJECT_ROOT/.uv-cache"

usage() {
  cat <<'EOF'
Usage: ./start.sh [--reset-venv] [--build-only] [--source-mode <local|remote>]

Options:
  --reset-venv   Delete .venv, reinstall the latest available Python with uv, recreate the virtualenv, and resync dependencies.
  --build-only   Rebuild generated docs and static site, but do not start the local preview server.
  --source-mode  Select docs source mode. Use 'local' for local folders and 'remote' for git sparse checkout.
EOF
}

stop_existing_server() {
  local pids
  pids="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null || true)"
  if [ -n "$pids" ]; then
    echo "Stopping existing preview server on $HOST:$PORT"
    kill $pids
  fi
}

reset_venv=false
build_only=false

while [ $# -gt 0 ]; do
  case "$1" in
    --reset-venv)
      reset_venv=true
      shift
      ;;
    --build-only)
      build_only=true
      shift
      ;;
    --source-mode)
      if [ $# -lt 2 ]; then
        echo "Missing value for --source-mode" >&2
        usage
        exit 1
      fi
      SOURCE_MODE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [ "$SOURCE_MODE" != "local" ] && [ "$SOURCE_MODE" != "remote" ]; then
  echo "Unsupported source mode: $SOURCE_MODE" >&2
  usage
  exit 1
fi

cd "$PROJECT_ROOT"

if [ "$reset_venv" = true ]; then
  rm -rf .venv
  uv python install --default
fi

if [ ! -d .venv ]; then
  uv python install --default
fi

uv sync
uv run python scripts/sync_sources.py --config "$CONFIG_PATH" --project-root . --source-mode "$SOURCE_MODE"
uv run python scripts/build_site.py --config "$CONFIG_PATH" --project-root . --output-dir "$OUTPUT_DIR" --source-mode "$SOURCE_MODE"
uv run mkdocs build -f "$PROJECT_ROOT/$OUTPUT_DIR/mkdocs.generated.yml" -d site

if [ "$build_only" = true ]; then
  echo "Static site rebuilt at $PROJECT_ROOT/$OUTPUT_DIR/site"
  exit 0
fi

stop_existing_server

echo "Preview: http://$HOST:$PORT/ (source mode: $SOURCE_MODE)"
exec uv run mkdocs serve -f "$PROJECT_ROOT/$OUTPUT_DIR/mkdocs.generated.yml" -a "$HOST:$PORT"
