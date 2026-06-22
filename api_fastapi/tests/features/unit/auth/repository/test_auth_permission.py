import pytest
from unittest.mock import AsyncMock, MagicMock

from app.features.auth.repository.permission_repository import PermissionRepository
from app.features.auth.entities.permission_entity import Permission
from app.features.auth.models.permission_model import PermissionModel


class TestAuthPermissionRepository:

    @pytest.mark.anyio
    async def test_create_permission_calls_session_methods(self):
        session = AsyncMock()

        # add() no AsyncSession normalmente é método síncrono
        session.add = MagicMock()

        async def fake_refresh(permission):
            permission.id = 1

        session.refresh.side_effect = fake_refresh

        payload = Permission(
            id=None,
            name="manage_users",
            description="Can manage users",
        )

        repository = PermissionRepository(session)

        result = await repository.create(payload)

        session.add.assert_called_once()
        added_model = session.add.call_args.args[0]
        assert isinstance(added_model, PermissionModel)
        assert added_model.name == "manage_users"
        assert added_model.description == "Can manage users"

        session.commit.assert_awaited_once()

        session.refresh.assert_awaited_once()
        refreshed_model = session.refresh.await_args.args[0]
        assert isinstance(refreshed_model, PermissionModel)

        assert result.id == 1
        assert result.name == "manage_users"
        assert result.description == "Can manage users"
        
    @pytest.mark.anyio
    async def test_list_permissions(self):
        session = AsyncMock()

        permission_models = [
            PermissionModel(id=1, name="manage_users", description="Can manage users"),
            PermissionModel(id=2, name="view_reports", description="Can view reports"),
        ]

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = permission_models
        session.execute = AsyncMock(return_value=mock_result)

        repository = PermissionRepository(session)

        result = await repository.list_permissions()

        session.execute.assert_awaited_once()
        assert result == [
            Permission(id=1, name="manage_users", description="Can manage users"),
            Permission(id=2, name="view_reports", description="Can view reports"),
        ]