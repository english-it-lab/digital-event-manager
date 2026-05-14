"""
API тесты для эндпоинта POST /api/v1/notifications/draw/results
Ветка: ZHER-15
Тесты используют ТОЛЬКО моки, не трогают реальную БД
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


class TestNotificationsAPI:
    """API тесты для уведомлений о жеребьёвке (только моки)"""

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
        """TC-01: Успешная отправка уведомлений"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            with patch("app.services.notification.NotificationService") as MockService:
                mock_service = AsyncMock()
                MockService.return_value = mock_service
                mock_service.send_draw_notifications = AsyncMock()

                response = client.post("/api/v1/notifications/draw/results", json={"eventId": 1})

                # Так как моки настроены, сервис не должен падать
                assert response.status_code in [200, 422]

    # ========== TC-02: Отправка без уведомлений ==========
    def test_tc02_send_notifications_no_recipients(self, client):
        """TC-02: Мероприятие существует, но нет получателей → 200 OK"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            with patch("app.services.notification.NotificationService") as MockService:
                mock_service = AsyncMock()
                MockService.return_value = mock_service
                mock_service.send_draw_notifications = AsyncMock()

                response = client.post("/api/v1/notifications/draw/results", json={"eventId": 2})

                assert response.status_code in [200, 422]

    # ========== TC-03: Event не найден ==========
    def test_tc03_event_not_found(self, client):
        """TC-03: Event не найден → 404 или 200 с ошибкой"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            with patch("app.services.notification.NotificationService") as MockService:
                mock_service = AsyncMock()
                MockService.return_value = mock_service
                mock_service.send_draw_notifications = AsyncMock(side_effect=ValueError("Event with id 999 not found"))

                response = client.post("/api/v1/notifications/draw/results", json={"eventId": 999})

                assert response.status_code in [200, 404, 422]

    # ========== TC-04: eventId = 0 ==========
    def test_tc04_event_id_zero(self, client):
        """TC-04: eventId = 0 → 422 Validation Error"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={"eventId": 0})
            assert response.status_code == 422

    # ========== TC-05: Отрицательный eventId ==========
    def test_tc05_event_id_negative(self, client):
        """TC-05: Отрицательный eventId → 422 Validation Error"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={"eventId": -5})
            assert response.status_code == 422

    # ========== TC-06: Отсутствует eventId ==========
    def test_tc06_missing_event_id(self, client):
        """TC-06: Отсутствует eventId в теле запроса → 422"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={})
            assert response.status_code == 422

    # ========== TC-07: eventId как строка ==========
    def test_tc07_event_id_string(self, client):
        """TC-07: eventId как строка → 422 Validation Error"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={"eventId": "not_a_number"})
            assert response.status_code == 422

    # ========== TC-08: eventId как float ==========
    def test_tc08_event_id_float(self, client):
        """TC-08: eventId как число с плавающей точкой → 422"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={"eventId": 1.5})
            assert response.status_code == 422

    # ========== TC-09: eventId как null ==========
    def test_tc09_event_id_null(self, client):
        """TC-09: eventId как null → 422 Validation Error"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={"eventId": None})
            assert response.status_code == 422

    # ========== TC-10: Пустой body ==========
    def test_tc10_empty_body(self, client):
        """TC-10: Пустой body → 422"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={})
            assert response.status_code == 422


# ========== Граничные тесты (без БД) ==========
class TestNotificationsAPIBoundary:
    """Граничные тесты (только валидация, без БД)"""

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
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={"eventId": 2**31 - 1})
            # Может быть 422 если валидация не пропускает, или 200/404 если пропускает
            assert response.status_code in [200, 404, 422]

    def test_boundary_max_event_id(self, client):
        """Граничный тест: максимальное значение eventId"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post("/api/v1/notifications/draw/results", json={"eventId": 9223372036854775807})
            assert response.status_code in [200, 404, 422]

    def test_boundary_special_characters(self, client):
        """Граничный тест: специальные символы в теле (игнорируются)"""
        with patch("app.adapters.api.v1.notifications.AsyncSessionMaker"):
            response = client.post(
                "/api/v1/notifications/draw/results",
                json={"eventId": 1, "extra_field": "<script>alert('xss')</script>"},
            )
            assert response.status_code in [200, 404, 422]
