import pytest

from app.features.auth.application.service.auth_roles_service import RolesService
from app.features.auth.infra.repository.roles_repository import RolesRepository
from app.features.auth.api.schemas.auth_roles_schema import RolesPermission


class TestAuthRolesService:
    
    @pytest.fixture(autouse=True)
    async def setup(self, async_session):
        self.async_session = async_session
        self.role_repository = RolesRepository(session=self.async_session)
        self.roles_service = RolesService(
            roles_repository=self.role_repository
        )
    
    @pytest.mark.anyio
    async def test_auth_roles_list(self, add_roles):
        retorno = await self.roles_service.list_roles()
        assert retorno is not None
        assert len(retorno[1].permission) == 0
        
    @pytest.mark.anyio
    async def test_auth_roles_implement_permission(self, add_roles, add_permission):
        service_roles = await self.roles_service.permission_implements(
            payload=RolesPermission(
                id=1,
                permission=[2, 3]
            )
        )
        
        assert service_roles is not None
        assert service_roles.permission[1].id == 3
        