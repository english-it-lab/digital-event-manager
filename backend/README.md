# Digital Event Manager API

FastAPI + PostgreSQL backend bootstrapped with **uv**, **SQLAlchemy 2.0**, and **Alembic**. The codebase follows a layered layout (repository → service → adapter) so that persistence, business rules, and delivery stay isolated.

## Requirements
- Python 3.13
- [uv](https://github.com/astral-sh/uv) (already recorded via `pyproject.toml` + `uv.lock`)
- Docker (optional but recommended for local infra)

## Installation
```bash
cd backend
uv sync                # installs dependencies into .venv
cp .env.example .env   # customise credentials if needed
```
Use `uv run <command>` to execute anything inside the virtual environment, e.g. `uv run uvicorn app.main:app --reload`.

### Generate API

#### Requirements
- **Python 3.12**
- **C++ Build Tools**
- **Rust toolchain**

After all dependencies are installed, run the generation script:

**Windows**
```bash
.\generate_api.bat
```

**Linux / macOS**
```bash
./generate_api.sh
```


## Project layout
```
app/
  adapters/api        # FastAPI routers + dependencies (delivery layer)
  core                # configuration
  db                  # async engine and sessions
  models              # SQLAlchemy ORM models (metadata used by Alembic)
  repositories        # persistence layer
  schemas             # Pydantic DTOs
  services            # business logic layer
alembic/              # migration environment + versions
Dockerfile            # production image built with uv
```

## Running locally
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or spin up everything (API + PostgreSQL) via Docker Compose:
```bash
cd backend
docker compose up --build
```
Compose exposes API on `http://localhost:8000` and Postgres on `localhost:5432` with the credentials defined in `.env`.

## Database migrations
```bash
# create a new revision
uv run alembic revision --autogenerate -m "short message"

# apply migrations
uv run alembic upgrade head

# apply inside running docker compose stack (defaults to `api` service)
./scripts/migrate.sh            # or ./scripts/migrate.sh <service-name>
CONTAINER_ID=abc123 ./scripts/migrate.sh  # override auto-detected container
```
Alembic already knows about the async metadata via `app.models.Base`.

## Sample flow (Universities)
1. **Schema** – `app/schemas/university.py`
2. **Repository** – `app/repositories/university.py`
3. **Service** – `app/services/university.py`
4. **Adapter** – `app/adapters/api/v1/universities.py`

When adding new features/entities, repeat the same pattern so that routers depend only on services and never on repositories directly.

## Swagger UI

After starting the API server, you can open the interactive Swagger UI in your browser:

```bash
http://localhost:8000/docs
```
