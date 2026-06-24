import os
from fastapi import HTTPException
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from app.features.auth.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")

@pytest.fixture
def client() -> TestClient:
    os.environ.setdefault("POSTGRES_USER", "test_user")
    os.environ.setdefault("POSTGRES_PASSWORD", "test_password")
    os.environ.setdefault("POSTGRES_DB", "test_db")
    os.environ.setdefault("POSTGRES_HOST", "localhost")
    os.environ.setdefault("POSTGRES_PORT", "5432")

    from app.main import app

    return TestClient(app)

class FakeAuthService:
    async def register(self, payload: RegisterRequest) -> UserResponse:
        return UserResponse(
            id=1,
            name=payload.name,
            email=payload.email,
            is_active=True,
            roles=[],
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