from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.adapters.api.dependencies import get_person_service
from app.adapters.api.v1.AuthAdapter import get_jwt_payload_dep
from app.main import app
from app.services.jwt import AuthPayload

client = TestClient(app)

mock_person_data = {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": None,
    "email": "john@example.com",
    "title": "Mr.",
    "degree": "PhD",
    "position": "Engineer",
    "workplace": "Company Inc.",
    "tg_name": "@johndoe",
}

mock_person_update = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "title": "Mr.",
    "position": "Senior Engineer",
}


@pytest.fixture
def mock_person_service():
    service = MagicMock()

    service.get_person_by_id = AsyncMock(return_value=mock_person_data)
    service.put_person = AsyncMock(return_value=mock_person_data)
    service.update_person = AsyncMock(return_value=mock_person_data)
    service.create_person = AsyncMock(return_value=mock_person_data)

    return service


@pytest.fixture
def mock_auth_payload():
    return AuthPayload(
        PERSON_ID=1,
        EXPIRATION_DATE=9999999999,  # далеко в будущем
    )


@pytest.fixture(autouse=True)
def override_dependencies(mock_person_service, mock_auth_payload):
    app.dependency_overrides[get_person_service] = lambda: mock_person_service
    app.dependency_overrides[get_jwt_payload_dep] = lambda: mock_auth_payload
    yield
    app.dependency_overrides.clear()


# ---------- Тесты для PUT /person ----------
def test_put_person_success(mock_person_service):
    """Тест успешного обновления/создания пользователя (PUT)"""
    response = client.put("/person/", json=mock_person_update)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["first_name"] == "John"
    mock_person_service.put_person.assert_called_once_with(1, mock_person_update)


def test_put_person_unauthorized(mock_person_service, mock_auth_payload):
    """Тест PUT без авторизации (переопределяем зависимость на исключение)"""

    async def raise_401():
        raise HTTPException(status_code=401, detail="missing token")

    app.dependency_overrides[get_jwt_payload_dep] = raise_401
    response = client.put("/person/", json=mock_person_update)
    assert response.status_code == 401
    mock_person_service.put_person.assert_not_called()
    app.dependency_overrides[get_jwt_payload_dep] = lambda: mock_auth_payload


# ---------- Тесты для POST /person ----------
def test_create_person_success(mock_person_service):
    """Тест успешного создания пользователя (POST)"""
    response = client.post("/person/", json=mock_person_update)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    mock_person_service.create_person.assert_called_once_with(1, mock_person_update)


def test_create_person_conflict(mock_person_service):
    """Тест создания уже существующего пользователя (409 Conflict)"""
    from fastapi import HTTPException

    mock_person_service.create_person = AsyncMock(
        side_effect=HTTPException(status_code=409, detail="Person with id 1 doesn't exist")
    )
    response = client.post("/person/", json=mock_person_update)
    assert response.status_code == 409
    assert "doesn't exist" in response.json()["detail"]


# ---------- Тесты для PATCH /person ----------
def test_update_person_success(mock_person_service):
    """Тест частичного обновления данных пользователя"""
    response = client.patch("/person/", json={"position": "Lead Engineer"})

    assert response.status_code == 200
    assert response.json()["id"] == 1
    called_args = mock_person_service.update_person.call_args
    assert called_args[0][0] == 1  # person_id
    assert called_args[0][1] == {"position": "Lead Engineer"}  # payload


def test_update_person_not_found(mock_person_service):
    """Тест обновления несуществующего пользователя (409 Conflict)"""
    mock_person_service.update_person = AsyncMock(
        side_effect=HTTPException(status_code=409, detail="Person with id 1 doesn't exist")
    )
    response = client.patch("/person/", json={"first_name": "Jane"})
    assert response.status_code == 409


# ---------- Тесты для GET /person (по query-параметру) ----------
def test_get_person_by_id_success(mock_person_service):
    """Тест получения пользователя по ID через query-параметр"""
    response = client.get("/person/?person_id=1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    mock_person_service.get_person_by_id.assert_called_once_with(1)


def test_get_person_by_id_not_found(mock_person_service):
    """Тест получения несуществующего пользователя"""
    mock_person_service.get_person_by_id = AsyncMock(
        side_effect=HTTPException(status_code=404, detail="Person with id 999 not found")
    )
    response = client.get("/person/?person_id=999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# ---------- Тесты для GET /person/me ----------
def test_get_me_success(mock_person_service, mock_auth_payload):
    """Тест получения данных текущего пользователя из JWT"""
    response = client.get("/person/me")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    mock_person_service.get_person_by_id.assert_called_once_with(mock_auth_payload.PERSON_ID)


def test_get_me_not_found(mock_person_service):
    """Тест: пользователь из JWT не найден в БД"""
    mock_person_service.get_person_by_id = AsyncMock(
        side_effect=HTTPException(status_code=404, detail="Person not found")
    )
    response = client.get("/person/me")
    assert response.status_code == 404


def test_get_me_unauthorized():
    """Тест запроса /me без авторизации"""

    async def raise_401():
        raise HTTPException(status_code=401, detail="missing token")

    app.dependency_overrides[get_jwt_payload_dep] = raise_401
    response = client.get("/person/me")
    assert response.status_code == 401
