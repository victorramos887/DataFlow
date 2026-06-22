from collections.abc import Generator

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.features.auth.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


class FakeAuthService:
    async def register(self, payload: RegisterRequest) -> UserResponse:
        return UserResponse(
            id=1,
            name=payload.name,
            email=payload.email,
            is_active=True,
        )

    async def login(self, payload: LoginRequest) -> TokenResponse:
        if payload.email != "victor@email.com" or payload.password != "12345678":
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        return TokenResponse(access_token="fake-jwt-token")


@pytest.fixture
def auth_client() -> Generator[TestClient]:
    from app.features.auth.dependencies.auth_dependencies import get_auth_service
    from app.main import app

    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_register_user(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={
            "name": "Victor Ramos",
            "email": "victor@email.com",
            "password": "12345678",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Victor Ramos",
        "email": "victor@email.com",
        "is_active": True,
    }


def test_login_user(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/login",
        json={
            "email": "victor@email.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "fake-jwt-token",
        "token_type": "bearer",
    }


def test_login_with_invalid_credentials(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/login",
        json={
            "email": "victor@email.com",
            "password": "senha-errada",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Credenciais inválidas"}