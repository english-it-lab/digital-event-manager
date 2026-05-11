"""
API тесты для эндпоинта POST /api/v1/notifications/draw/results
Ветка: ZHER-15
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


class TestNotificationsAPI:
    """
    Тест-кейсы для API уведомлений о жеребьёвке
    Покрытие: TC-01 до TC-12
    """

    # =========================================================
    # Фикстуры
    # =========================================================

    @pytest.fixture
    def client(self):
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
        return TestClient(app)

    @pytest.fixture
    def mock_notification_service(self):
        """Мок для NotificationService"""
        with patch('app.adapters.api.v1.notifications.NotificationService') as mock:
            service_instance = AsyncMock()
            mock.return_value = service_instance
            yield service_instance

    @pytest.fixture
    def mock_session_maker(self):
        """Мок для AsyncSessionMaker"""
        with patch('app.adapters.api.v1.notifications.AsyncSessionMaker') as mock:
            session_instance = AsyncMock()
            mock.return_value.__aenter__.return_value = session_instance
            yield mock

    # =========================================================
    # Позитивные тесты
    # =========================================================

    # TC-01: Успешная отправка уведомлений
    def test_tc01_send_notifications_success(self, client, mock_notification_service):
        """
        TC-01: Успешная отправка уведомлений
        """
        # Arrange
        mock_notification_service.return_value.send_draw_notifications = AsyncMock()

        # Act
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 1}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "успешно" in data.get("message", "").lower()
        mock_notification_service.return_value.send_draw_notifications.assert_called_once_with(1)

    # TC-02: Отправка без уведомлений (нет участников)
    def test_tc02_send_notifications_no_recipients(self, client, mock_notification_service):
        """
        TC-02: Мероприятие существует, но нет получателей → 200 OK
        """
        # Arrange
        mock_notification_service.return_value.send_draw_notifications = AsyncMock()

        # Act
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 2}
        )

        # Assert
        assert response.status_code == 200
        mock_notification_service.return_value.send_draw_notifications.assert_called_once_with(2)

    # =========================================================
    # Негативные тесты - ошибки клиента (4xx)
    # =========================================================

    # TC-03: Event не найден
    def test_tc03_event_not_found(self, client, mock_notification_service):
        """
        TC-03: Event не найден → 404
        """
        # Arrange
        mock_notification_service.return_value.send_draw_notifications = AsyncMock(
            side_effect=ValueError("Event with id 999 not found")
        )

        # Act
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 999}
        )

        # Assert
        assert response.status_code == 404
        error_text = str(response.json()).lower()
        assert "not found" in error_text or "не найдено" in error_text

    # TC-04: eventId = 0
    def test_tc04_event_id_zero(self, client):
        """
        TC-04: eventId = 0 → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 0}
        )
        assert response.status_code == 422

    # TC-05: Отрицательный eventId
    def test_tc05_event_id_negative(self, client):
        """
        TC-05: Отрицательный eventId → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": -5}
        )
        assert response.status_code == 422

    # TC-06: Отсутствует eventId
    def test_tc06_missing_event_id(self, client):
        """
        TC-06: Отсутствует eventId в теле запроса → 422
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={}
        )
        assert response.status_code == 422

    # TC-07: eventId как строка
    def test_tc07_event_id_string(self, client):
        """
        TC-07: eventId как строка → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": "not_a_number"}
        )
        assert response.status_code == 422

    # TC-08: eventId как float
    def test_tc08_event_id_float(self, client):
        """
        TC-08: eventId как число с плавающей точкой → 422
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 1.5}
        )
        assert response.status_code == 422

    # TC-09: eventId как null
    def test_tc09_event_id_null(self, client):
        """
        TC-09: eventId как null → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": None}
        )
        assert response.status_code == 422

    # TC-10: Пустой body
    def test_tc10_empty_body(self, client):
        """
        TC-10: Пустой body → 422
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            content=b""
        )
        assert response.status_code == 422

    # =========================================================
    # Негативные тесты - ошибки сервера (5xx)
    # =========================================================

    # TC-11: Ошибка подключения к БД
    def test_tc11_database_error(self, client, mock_notification_service):
        """
        TC-11: Ошибка БД → 500 Internal Server Error
        """
        # Arrange
        mock_notification_service.return_value.send_draw_notifications = AsyncMock(
            side_effect=Exception("Database connection failed")
        )

        # Act
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 1}
        )

        # Assert
        assert response.status_code == 500

    # TC-12: Ошибка SMTP
    def test_tc12_smtp_error(self, client, mock_notification_service):
        """
        TC-12: Ошибка SMTP сервера → 500 Internal Server Error
        """
        # Arrange
        mock_notification_service.return_value.send_draw_notifications = AsyncMock(
            side_effect=Exception("SMTP server connection refused")
        )

        # Act
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 1}
        )

        # Assert
        assert response.status_code == 500


# =========================================================
# Дополнительные тесты для покрытия граничных случаев
# =========================================================

class TestNotificationsAPIBoundary:
    """Граничные тесты"""

    @pytest.fixture
    def client(self):
        try:
            from main import app
            return TestClient(app)
        except ImportError:
            from fastapi import FastAPI
            return TestClient(FastAPI())

    # Большое значение eventId
    def test_boundary_large_event_id(self, client):
        """
        Граничный тест: очень большое значение eventId
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 2 ** 31 - 1}  # Max int32
        )
        # Может быть 200 или 404 в зависимости от наличия такого ID
        assert response.status_code in [200, 404]

    # Максимальное значение eventId
    def test_boundary_max_event_id(self, client):
        """
        Граничный тест: максимальное значение eventId
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 9223372036854775807}  # Max int64
        )
        assert response.status_code in [200, 404, 422]

    # Специальные символы в теле (не влияют, так как eventId - число)
    def test_boundary_special_characters(self, client):
        """
        Граничный тест: специальные символы в теле
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 1, "extra_field": "<script>alert('xss')</script>"}
        )
        # Дополнительные поля должны игнорироваться или вызывать ошибку
        assert response.status_code in [200, 422]
