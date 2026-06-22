import pytest
from unittest.mock import AsyncMock, MagicMock

from app.features.auth.entities.user_entity import User
from app.features.auth.schemas.auth_schema import RegisterRequest
from app.features.auth.service.auth_service import AuthService


@pytest.mark.anyio
async def test_register_user_success() -> None:
    user_repository = MagicMock()
    password_hasher = MagicMock()

    user_repository.get_by_email = AsyncMock(return_value=None)
    password_hasher.hash_password.return_value = "hashed-password"

    user_repository.create = AsyncMock(return_value=User(
        id=1,
        name="Victor Ramos",
        email="victor@email.com",
        password_hash="hashed-password",
        is_active=True,
    ))

    service = AuthService(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )
    result = await service.register(
        RegisterRequest(
            name="Victor Ramos",
            email="victor@email.com",
            password="password5678",
        )
    )

    assert result.id == 1
    assert result.name == "Victor Ramos"
    assert result.email == "victor@email.com"
    assert result.is_active is True

    user_repository.get_by_email.assert_called_once_with("victor@email.com")
    password_hasher.hash_password.assert_called_once_with("password5678")
    user_repository.create.assert_called_once()