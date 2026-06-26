
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.features.auth.api.dependencies.auth_dependencies import get_auth_service


class FakeUser:
    id = 1


class FakeAuthService:
    async def authenticate(self, email: str, password: str):
        return FakeUser()

class FakeAuthServiceInvalidCredentials:
    async def authenticate(self, email: str, password: str):
        return None

class TestAuthUserController:  
    
    @pytest.mark.anyio
    def test_register_user(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/auth/user/register",
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
            "roles":[],
            "is_active": True,
        }

    @pytest.mark.anyio
    async def test_login_success(self):
        app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/auth/user/login",
                data={
                    "username": "user@email.com",
                    "password": "123456",
                },
            )

        app.dependency_overrides.clear()

        assert response.status_code == 200

        body = response.json()

        assert body["token_type"] == "bearer"
        assert "access_token" in body
        assert isinstance(body["access_token"], str)

    @pytest.mark.anyio
    async def test_login_with_invalid_credentials(self) -> None:
        app.dependency_overrides[get_auth_service] = (
            lambda: FakeAuthServiceInvalidCredentials()
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/auth/user/login",
                data={
                    "username": "user@email.com",
                    "password": "wrong-password",
                },
            )

        app.dependency_overrides.clear()

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Invalid email or password"
        }