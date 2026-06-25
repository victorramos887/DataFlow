
import pytest
from fastapi.testclient import TestClient


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
    def test_login_user(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/auth/user/login",
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

    @pytest.mark.anyio
    def test_login_with_invalid_credentials(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/auth/user/login",
            json={
                "email": "victor@email.com",
                "password": "senha-errada",
            },
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Credenciais inválidas"}