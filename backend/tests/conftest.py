import os
from unittest.mock import AsyncMock, Mock, patch

import pytest

# ========== Настройки переменных окружения для тестов ==========
os.environ.setdefault("EMAIL_PASSWORD", "test-password")
os.environ.setdefault("EMAIL_LOGIN", "test@example.com")
os.environ.setdefault("SMTP_SERVER", "smtp.example.com")


# ========== Фикстуры для моков БД и сервисов ==========


@pytest.fixture
def mock_db_session():
    """Мок для сессии БД (для юнит-тестов)"""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.scalar = AsyncMock()
    session.add = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def mock_send_email():
    """Мок для функции отправки писем"""
    with patch("app.services.send_mails.send_email") as mock:
        yield mock


@pytest.fixture
def mock_async_session_maker():
    """Мок для AsyncSessionMaker (для API тестов)"""
    with patch("app.adapters.api.v1.notifications.AsyncSessionMaker") as mock:
        mock_session = AsyncMock()
        mock.return_value.__aenter__.return_value = mock_session
        yield mock


@pytest.fixture
def mock_event_repository():
    """Мок для EventRepository"""
    with patch("app.repositories.event.EventRepository") as mock:
        repo = Mock()
        repo.get_by_id = AsyncMock()
        repo.exists_by_id = AsyncMock()
        mock.return_value = repo
        yield repo


@pytest.fixture
def mock_notification_repository():
    """Мок для NotificationRepository"""
    with patch("app.repositories.notification.NotificationRepository") as mock:
        repo = Mock()
        repo.get_notification_payload = AsyncMock()
        mock.return_value = repo
        yield repo


# ========== Фикстура для создания тестового клиента ==========


@pytest.fixture
def test_client():
    """Тестовый клиент FastAPI"""
    try:
        from main import app
    except ImportError:
        try:
            from app.main import app
        except ImportError:
            from fastapi import FastAPI

            app = FastAPI()
            try:
                from app.adapters.api.v1 import router

                app.include_router(router, prefix="/api/v1")
            except ImportError:
                pass

    from fastapi.testclient import TestClient

    return TestClient(app)
