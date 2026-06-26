# tests/features/unit/auth/infra/repository/test_auth_user_repository.py

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from app.features.auth.domain.entities.user_entity import User
from app.features.auth.infra.repository.user_repository import UserRepository


class TestAuthUserRepository:
    def setup_method(self):
        self.session = Mock()
        self.repository = UserRepository(session=self.session)

    @pytest.mark.anyio
    async def test_get_by_email_success(self) -> None:
        user_model = SimpleNamespace(
            id=1,
            name="Victor Ramos",
            email="victor@email.com",
            password_hash="hashed-password",
            is_active=True,
        )

        result_mock = Mock()
        result_mock.scalar_one_or_none.return_value = user_model

        self.session.execute = AsyncMock(return_value=result_mock)

        result = await self.repository.get_by_email("victor@email.com")

        assert isinstance(result, User)
        assert result.id == 1
        assert result.name == "Victor Ramos"
        assert result.email == "victor@email.com"
        assert result.password_hash == "hashed-password"
        assert result.is_active is True

        self.session.execute.assert_awaited_once()
        result_mock.scalar_one_or_none.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_email_not_found(self) -> None:
        result_mock = Mock()
        result_mock.scalar_one_or_none.return_value = None

        self.session.execute = AsyncMock(return_value=result_mock)

        result = await self.repository.get_by_email("notfound@email.com")

        assert result is None

        self.session.execute.assert_awaited_once()
        result_mock.scalar_one_or_none.assert_called_once()