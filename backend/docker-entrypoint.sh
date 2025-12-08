#!/bin/bash
set -e

echo "Waiting for database to be ready..."
# БД уже ожидается через depends_on + healthcheck

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting application..."
exec "$@"
