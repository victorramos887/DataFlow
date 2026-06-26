from unittest.mock import AsyncMock
import pytest

from app.features.auth.api.controller.auth_roles_controller import post_roles
from app.features.auth.api.schemas.auth_roles_schema import RolesRequest

class TestAuthRoles:
    @pytest.mark.anyio
    async def test_post_roles(self) -> None:
        service = AsyncMock()
        service.create_roles.return_value = {
            "message": "Roles created sucess"
        }
    
        payload = RolesRequest(
            name = "dashboard.view",
            description="Can view dashboard"
        )
        
        result =  await post_roles(payload=payload, service=service)
        
        assert result == {"message": "Roles created sucess"}
        service.create_roles.assert_awaited_once_with(payload)