#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-main}"
SITE_DIR="${SITE_DIR:-$PROJECT_ROOT/site}"
SKIP_GIT_PULL="${SKIP_GIT_PULL:-0}"
DOCKER_COMPOSE_FILE="${DOCKER_COMPOSE_FILE:-$PROJECT_ROOT/deploy/docker-compose.yml}"
RELOAD_HOST_NGINX="${RELOAD_HOST_NGINX:-1}"
DOCS_INTERNAL_DOCKER_NETWORK="${DOCS_INTERNAL_DOCKER_NETWORK:-docs-auth-internal}"
DOCS_REDIS_DOCKER_NETWORK="${DOCS_REDIS_DOCKER_NETWORK:-webapp_wps_net}"
DOCS_SOURCE_MODE="${DOCS_SOURCE_MODE:-remote}"

cd "$PROJECT_ROOT"

if [[ "$SKIP_GIT_PULL" != "1" ]]; then
  git fetch --all --prune
  git checkout "$DEPLOY_BRANCH"
  git pull --ff-only origin "$DEPLOY_BRANCH"
fi

uv sync
uv run python scripts/sync_sources.py --config config/source-repos.json --project-root "$PROJECT_ROOT" --source-mode "$DOCS_SOURCE_MODE"
uv run python scripts/build_site.py --config config/source-repos.json --project-root "$PROJECT_ROOT" --output-dir .generated --source-mode "$DOCS_SOURCE_MODE"
uv run mkdocs build -f "$PROJECT_ROOT/.generated/mkdocs.generated.yml" -d "$SITE_DIR"

if [[ ! -f "$PROJECT_ROOT/deploy/casdoor/app.conf" ]]; then
  echo "missing deploy/casdoor/app.conf" >&2
  exit 1
fi

if [[ ! -f "$PROJECT_ROOT/deploy/oauth2-proxy/oauth2-proxy.cfg" ]]; then
  echo "missing deploy/oauth2-proxy/oauth2-proxy.cfg" >&2
  exit 1
fi

export DOCS_INTERNAL_DOCKER_NETWORK DOCS_REDIS_DOCKER_NETWORK
docker compose -f "$DOCKER_COMPOSE_FILE" up -d

if [[ "$RELOAD_HOST_NGINX" == "1" ]]; then
  if [[ "${EUID}" -eq 0 ]]; then
    nginx -t
    if command -v systemctl >/dev/null 2>&1; then
      systemctl reload nginx
    else
      nginx -s reload
    fi
  else
    sudo nginx -t
    if command -v systemctl >/dev/null 2>&1; then
      sudo systemctl reload nginx
    else
      sudo nginx -s reload
    fi
  fi
fi
