import pytest
from unittest.mock import AsyncMock, MagicMock, Mock

from app.features.auth.domain.entities.user_entity import User
from app.features.auth.domain.entities.roles_entity import Role
from app.features.auth.api.schemas.auth_schema import RegisterRequest, UserRequestRole
from app.features.auth.application.service.auth_service import AuthService


class TestAuthUserService:
    
    def setup_method(self):
        self.user_repository = MagicMock()
        self.password_hasher = MagicMock()
        self.role_repository = MagicMock()
        
        self.service = AuthService(
            user_repository=self.user_repository,
            password_hasher=self.password_hasher,
            role_repository=self.role_repository
        )
        
    @pytest.mark.anyio
    async def test_register_user_success(self) -> None:
        
        self.user_repository.get_by_email = AsyncMock(return_value=None)
        self.role_repository.get_by_id = AsyncMock(return_value=None)
        self.password_hasher.hash_password.return_value = "hashed-password"

        self.user_repository.create = AsyncMock(return_value=User(
            id=1,
            name="Victor Ramos",
            email="victor@email.com",
            password_hash="hashed-password",
            is_active=True,
        ))
        
        result = await self.service.register(
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

        self.user_repository.get_by_email.assert_called_once_with("victor@email.com")
        self.password_hasher.hash_password.assert_called_once_with("password5678")
        self.user_repository.create.assert_called_once()
        
    @pytest.mark.anyio
    async def test_implement_roles_in_user_success(self) -> None:
        self.role_repository.get_by_id = AsyncMock(
            side_effect=[
                Role(id=1, name="admin", description="Admin role"),
                Role(id=2, name="viewer", description="Viewer role"),
            ]
        )
        self.user_repository.assign_roles = AsyncMock(
            return_value=User(
                id=1,
                name="Victor Ramos",
                email="victor@email.com",
                password_hash="hashed-password",
                is_active=True,
                roles=[
                    Role(id=1, name="admin", description="Admin role"),
                    Role(id=2, name="viewer", description="Viewer role"),
                ],
            )
        )
        
        result = await self.service.roles_implements(
            UserRequestRole(
                id=1,
                roles=[1, 2]
            )
        )
        
        assert result.id == 1
        assert result.roles == [1, 2]
        
    @pytest.mark.anyio
    async def test_authenticate_success(self) -> None:
        user = User(
            id=1,
            name="Victor Ramos",
            email="victor@email.com",
            password_hash="hashed-password",
            is_active=True,
            roles=[],
        )

        self.user_repository.get_by_email = AsyncMock(return_value=user)

        self.password_hasher.verify = AsyncMock(return_value=True)

        result = await self.service.authenticate(
            email="victor@email.com",
            password="123456",
        )

        assert result == user

        self.user_repository.get_by_email.assert_awaited_once_with(
            "victor@email.com"
        )

        self.password_hasher.verify.assert_called_once_with(
            plain_password="123456",
            hashed_password="hashed-password",
        )

    @pytest.mark.anyio
    async def test_authenticate_user_not_found(self) -> None:
        self.user_repository.get_by_email = AsyncMock(return_value=None)

        result = await self.service.authenticate(
            email="notfound@email.com",
            password="123456",
        )

        assert result is None

        self.user_repository.get_by_email.assert_awaited_once_with(
            "notfound@email.com"
        )

        self.password_hasher.verify.assert_not_called()

    @pytest.mark.anyio
    async def test_authenticate_invalid_password(self) -> None:
        user = User(
            id=1,
            name="Victor Ramos",
            email="victor@email.com",
            password_hash="hashed-password",
            is_active=True,
            roles=[],
        )

        self.user_repository.get_by_email = AsyncMock(return_value=user)

        self.password_hasher.verify = Mock(return_value=False)

        result = await self.service.authenticate(
            email="victor@email.com",
            password="wrong-password",
        )

        assert result is None

        self.password_hasher.verify.assert_called_once_with(
            plain_password="wrong-password",
            hashed_password="hashed-password",
        )

    @pytest.mark.anyio
    async def test_authenticate_inactive_user(self) -> None:
        user = User(
            id=1,
            name="Victor Ramos",
            email="victor@email.com",
            password_hash="hashed-password",
            is_active=False,
            roles=[],
        )

        self.user_repository.get_by_email = AsyncMock(return_value=user)

        self.password_hasher.verify = AsyncMock(return_value=True)

        result = await self.service.authenticate(
            email="victor@email.com",
            password="123456",
        )

        assert result is None