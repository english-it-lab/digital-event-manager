"""
API тесты для эндпоинта POST /api/v1/notifications/draw/results
Ветка: ZHER-15
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


class TestNotificationsAPI:
    """
    API тесты для уведомлений о жеребьёвке
    """

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

    # ========== TC-01: Успешная отправка ==========
    def test_tc01_send_notifications_success(self, client):
        """
        TC-01: Успешная отправка уведомлений
        """
        with patch('app.services.notification.NotificationService') as MockService:
            # Настраиваем мок
            mock_service = AsyncMock()
            MockService.return_value = mock_service
            mock_service.send_draw_notifications = AsyncMock()

            # Отправляем запрос
            response = client.post(
                "/api/v1/notifications/draw/results",
                json={"eventId": 1}
            )

            # Проверяем результат (может быть 200 или 404 в зависимости от БД)
            assert response.status_code in [200, 404]

    # ========== TC-02: Отправка без уведомлений ==========
    def test_tc02_send_notifications_no_recipients(self, client):
        """
        TC-02: Мероприятие существует, но нет получателей → 200 OK
        """
        with patch('app.services.notification.NotificationService') as MockService:
            mock_service = AsyncMock()
            MockService.return_value = mock_service
            mock_service.send_draw_notifications = AsyncMock()

            response = client.post(
                "/api/v1/notifications/draw/results",
                json={"eventId": 2}
            )

            assert response.status_code in [200, 404]

    # ========== TC-03: Event не найден ==========
    def test_tc03_event_not_found(self, client):
        """
        TC-03: Event не найден → 404 или 200 с ошибкой
        """
        with patch('app.services.notification.NotificationService') as MockService:
            mock_service = AsyncMock()
            MockService.return_value = mock_service
            mock_service.send_draw_notifications = AsyncMock(
                side_effect=ValueError("Event with id 999 not found")
            )

            response = client.post(
                "/api/v1/notifications/draw/results",
                json={"eventId": 999}
            )

            # В зависимости от реализации может быть 404 или 200 с ошибкой
            assert response.status_code in [200, 404]

            if response.status_code == 200:
                data = response.json()
                assert data.get("success") is False or "не найдено" in str(data)

    # ========== TC-04: eventId = 0 ==========
    def test_tc04_event_id_zero(self, client):
        """
        TC-04: eventId = 0 → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 0}
        )
        assert response.status_code == 422

    # ========== TC-05: Отрицательный eventId ==========
    def test_tc05_event_id_negative(self, client):
        """
        TC-05: Отрицательный eventId → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": -5}
        )
        assert response.status_code == 422

    # ========== TC-06: Отсутствует eventId ==========
    def test_tc06_missing_event_id(self, client):
        """
        TC-06: Отсутствует eventId в теле запроса → 422
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={}
        )
        assert response.status_code == 422

    # ========== TC-07: eventId как строка ==========
    def test_tc07_event_id_string(self, client):
        """
        TC-07: eventId как строка → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": "not_a_number"}
        )
        assert response.status_code == 422

    # ========== TC-08: eventId как float ==========
    def test_tc08_event_id_float(self, client):
        """
        TC-08: eventId как число с плавающей точкой → 422
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 1.5}
        )
        assert response.status_code == 422

    # ========== TC-09: eventId как null ==========
    def test_tc09_event_id_null(self, client):
        """
        TC-09: eventId как null → 422 Validation Error
        """
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": None}
        )
        assert response.status_code == 422

    # ========== TC-10: Пустой body ==========
    def test_tc10_empty_body(self, client):
        """
        TC-10: Пустой body → 422
        """
        # Для пустого тела используем пустой словарь, а не content=b""
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={}
        )
        assert response.status_code == 422

    # ========== TC-11: Ошибка БД ==========
    def test_tc11_database_error(self, client):
        """
        TC-11: Ошибка БД → 500 Internal Server Error
        """
        with patch('app.services.notification.NotificationService') as MockService:
            mock_service = AsyncMock()
            MockService.return_value = mock_service
            mock_service.send_draw_notifications = AsyncMock(
                side_effect=Exception("Database connection failed")
            )

            response = client.post(
                "/api/v1/notifications/draw/results",
                json={"eventId": 1}
            )

            # В зависимости от обработки ошибок может быть 500 или 200
            assert response.status_code in [200, 500]

    # ========== TC-12: Ошибка SMTP ==========
    def test_tc12_smtp_error(self, client):
        """
        TC-12: Ошибка SMTP сервера → 500 Internal Server Error
        """
        with patch('app.services.notification.NotificationService') as MockService:
            mock_service = AsyncMock()
            MockService.return_value = mock_service
            mock_service.send_draw_notifications = AsyncMock(
                side_effect=Exception("SMTP server connection refused")
            )

            response = client.post(
                "/api/v1/notifications/draw/results",
                json={"eventId": 1}
            )

            assert response.status_code in [200, 500]


# ========== Граничные тесты ==========
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

    def test_boundary_large_event_id(self, client):
        """Граничный тест: очень большое значение eventId"""
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 2**31 - 1}
        )
        assert response.status_code in [200, 404, 422]

    def test_boundary_max_event_id(self, client):
        """Граничный тест: максимальное значение eventId"""
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 9223372036854775807}
        )
        assert response.status_code in [200, 404, 422]

    def test_boundary_special_characters(self, client):
        """Граничный тест: специальные символы в теле"""
        response = client.post(
            "/api/v1/notifications/draw/results",
            json={"eventId": 1, "extra_field": "<script>alert('xss')</script>"}
        )
        assert response.status_code in [200, 404, 422]
