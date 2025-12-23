FROM python:3.12-slim AS base

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_CACHE_DIR=/app/.uv_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

RUN apt-get update && \
    apt-get install -y \
    openjdk-21-jdk \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY generate_api.sh /generate_api.sh
RUN chmod +x /generate_api.sh

COPY resources resources
COPY alembic alembic
COPY app app
COPY alembic.ini main.py ./

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
