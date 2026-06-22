from unittest.mock import AsyncMock

import pytest

from app.features.auth.controller.auth_permissions_controller import post_permission
from app.features.auth.schemas.auth_permission_schema import PermissionRequest


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
    
