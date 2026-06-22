import pytest

from app.features.auth.schemas.auth_permission_schema import PermissionRequest

class TestAuthPermissionSchemas:
    def test_permission_request_valid(self) -> None:
        payload = PermissionRequest(
            name="manage_users",
            description="Can manage users",
        )

        assert payload.name == "manage_users"
        assert payload.description == "Can manage users"