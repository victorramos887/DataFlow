from unittest.mock import AsyncMock

import pytest

from app.features.auth.api.controller.auth_permissions_controller import post_permission, get_permission
from app.features.auth.api.schemas.auth_permission_schema import PermissionRequest


class TestAuthPermission:
    @pytest.mark.anyio
    async def test_post_permission(self) -> None:
        service = AsyncMock()
        service.create_permission.return_value = {"message": "Permission created successfully"}

        payload = PermissionRequest(
            name="manage_users",
            description="Can manage users",
        )

        result = await post_permission(payload=payload, service=service)

        assert result == {"message": "Permission created successfully"}
        service.create_permission.assert_awaited_once_with(payload)
    
    @pytest.mark.anyio
    async def test_post_permission_already_exists(self) -> None:
        service = AsyncMock()
        service.create_permission.return_value = {"error": "Permission already exists"}

        payload = PermissionRequest(
            name="manage_users",
            description="Can manage users",
        )

        result = await post_permission(payload=payload, service=service)

        assert result == {"error": "Permission already exists"}
        service.create_permission.assert_awaited_once_with(payload)
        
    @pytest.mark.anyio
    async def test_list_permissions(self) -> None:
        service = AsyncMock()
        service.list_permission.return_value = [
            {"id": 1, "name": "manage_users", "description": "Can manage users"},
            {"id": 2, "name": "view_reports", "description": "Can view reports"},
        ]
        
        result = await service.list_permission()
        assert result == [
            {"id": 1, "name": "manage_users", "description": "Can manage users"},
            {"id": 2, "name": "view_reports", "description": "Can view reports"},
        ]
        service.list_permission.assert_awaited_once()
        
    @pytest.mark.anyio
    async def test_get_permission_by_id(self) -> None:
        service = AsyncMock()
        service.get_permission.return_value = {"id": 1, "name": "manage_users", "description": "Can manage users"}
        
        permission_id = 1
        result = await get_permission(permission_id=permission_id, service=service)
        assert result == {"id": 1, "name": "manage_users", "description": "Can manage users"}
        service.get_permission.assert_awaited_once_with(permission_id)