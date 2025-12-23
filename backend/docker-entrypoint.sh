#!/bin/sh
set -e

echo "Waiting for database to be ready..."
# БД уже ожидается через depends_on + healthcheck

echo "Running API generation..."
/generate_api.sh

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting application..."
exec "$@"
