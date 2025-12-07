# Digital Event Manager Backend

## Стек и инструменты
- **FastAPI** — HTTP-интерфейс и зависимость внедрения
- **SQLAlchemy 2.0 (async)** — модели и доступ к БД
- **Alembic** — миграции
- **PostgreSQL** — основная БД
- **uv** — менеджер зависимостей и запуск приложений/скриптов
- **Docker + docker-compose** — локальная инфраструктура (API + DB)

## Структура слоёв
```
backend/
└── app/
    ├── adapters/   # HTTP-адаптеры (роуты/зависимости FastAPI)
    ├── repositories/  # Работа с БД (SQLAlchemy)
    ├── services/   # Бизнес-логика и координация репозиториев
    ├── schemas/    # Pydantic-схемы для ввода/вывода
    ├── models/     # ORM-модели и metadata
    ├── db/         # Сессии/интеграция с БД
    └── core/       # Настройки
```

### Adapter (роуты)
- Расположены в `app/adapters/api`.
- Каждый модуль сообщает FastAPI как принимать вход, валидирует схему и вызывает сервисы.
- Пример: `app/adapters/api/v1/universities.py` импортирует сервис и описывает эндпоинты `GET/POST /universities`.

### Service
- Находится в `app/services`.
- Инкапсулирует бизнес-правила и сценарии использования.
- Работает с несколькими репозиториями, не зависит от FastAPI.

### Repository
- В `app/repositories`.
- Отвечает только за чтение/запись данных через SQLAlchemy (async `AsyncSession`).
- Возвращает ORM-объекты, которыми пользуются сервисы.

## Инициализация окружения
```bash
cd backend
uv sync                # создаёт .venv и ставит зависимости
cp .env.example .env   # переопределите секреты при необходимости
```

## Миграции
```bash
uv run alembic upgrade head   # применить
uv run alembic revision -m "<описание>" --autogenerate   # создать (DB должна быть доступна)
```

## Docker
```bash
cd backend
docker compose up --build
```
Компоуз поднимает `api` (FastAPI + uvicorn) и `db` (PostgreSQL 16). API автоматически подхватывает настройки из `.env`.

## Полезные команды
- `uv run uvicorn app.main:app --reload` — локальный запуск с авто-перезагрузкой.
- `uv run pytest` — добавить, когда появятся тесты.

## Следующие шаги
1. Добавляйте новые сущности, повторяя паттерн `schema -> repository -> service -> adapter`.
2. Расширяйте схемы/валидацию и покрывайте интеграцию тестами.
