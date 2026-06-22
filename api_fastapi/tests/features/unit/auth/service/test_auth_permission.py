from unittest.mock import AsyncMock

import pytest

from app.features.auth.entities.permission_entity import Permission
from app.features.auth.schemas.auth_permission_schema import PermissionRequest, PermissionResponse
from app.features.auth.service.auth_permission_service import PermissionService


class TestAuthPermissionService:

    @pytest.mark.anyio
    async def test_create_permission(self) -> None:
        repository_mock = AsyncMock()

        payload = PermissionRequest(
            name="manage_users",
            description="Can manage users",
        )

        expected_permission = PermissionResponse(
            id=1,
            name="manage_users",
            description="Can manage users",
        )

        repository_mock.get_by_name.return_value = None
        repository_mock.create.return_value = expected_permission

        service = PermissionService(repository_mock)

        result = await service.create_permission(payload)

        assert result == expected_permission
        repository_mock.get_by_name.assert_awaited_once_with("manage_users")

        repository_mock.create.assert_awaited_once()
        created_permission_arg = repository_mock.create.await_args.args[0]
        assert isinstance(created_permission_arg, Permission)
        assert created_permission_arg.id is None
        assert created_permission_arg.name == "manage_users"
        assert created_permission_arg.description == "Can manage users"