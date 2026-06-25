import os
from fastapi import HTTPException
from collections.abc import Generator, AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from app.features.auth.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.dependencies import get_async_session
from app.features.auth.dependencies.auth_dependencies import get_auth_service
from app.main import app

from app.core.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

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
    
    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
async def auth_integration_client(
    async_session: AsyncSession,
) -> AsyncGenerator[TestClient, None]:

    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        yield async_session

    app.dependency_overrides.clear()
    app.dependency_overrides[get_async_session] = override_get_async_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    SessionTesting = async_sessionmaker(
        bind = engine,
        expire_on_commit=False,
    )
    
    async with SessionTesting() as session:
        yield session
        
    await engine.dispose()