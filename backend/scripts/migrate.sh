#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${1:-api}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

container_id="${CONTAINER_ID:-$(docker compose -f "$PROJECT_DIR/docker-compose.yml" ps -q "$SERVICE_NAME" 2>/dev/null || true)}"

if [[ -z "$container_id" ]]; then
  echo "Could not find running container for service '$SERVICE_NAME'." >&2
  echo "Start the stack with 'docker compose up -d' and try again, or set CONTAINER_ID manually." >&2
  exit 1
fi

exec docker exec -it "$container_id" uv run alembic upgrade head
