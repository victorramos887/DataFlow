import pytest
from app.features.auth.api.schemas.auth_roles_schema import RolesRequest, RolesResponse

class TestAuthRoleSchemas:
    def test_roles_request_valid(self) -> None:
        payload = RolesRequest(
            name = "edit_manage_users",
            description="Pode Editar usuários"
        )
        
        assert payload.name == "edit_manage_users"
        assert payload.description == "Pode Editar usuários"
        
    def test_roles_response_valid(self) -> None:
        payload = RolesResponse(
            id=1,
            name="edit_manage_users",
            description="Pode Editar usuários"
        )
        
        assert payload.name == "edit_manage_users"
        assert payload.description == "Pode Editar usuários"
        assert payload.permission == []
        assert payload.users == []