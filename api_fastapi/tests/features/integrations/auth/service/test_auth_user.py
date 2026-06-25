import pytest

from app.features.auth.schemas.auth_schema import RegisterRequest
from app.features.auth.service.auth_service import AuthService

from app.features.auth.repository.user_repository import UserRepository
from app.features.auth.repository.roles_repository import RolesRepository
from app.features.auth.security.password_hasher import PasswordHasher
from app.features.auth.schemas.auth_schema import UserRequestRole

class TestAuthUserServiceIntegration:
    
    @pytest.fixture(autouse=True)
    async def setup(self, async_session, auth_integration_client):
        self.async_session = async_session
        self.auth_client = auth_integration_client
        self.user_repository = UserRepository(session=self.async_session)
        self.role_repository = RolesRepository(session=self.async_session)
        self.password_hasher = PasswordHasher()

        self.service = AuthService(
            user_repository=self.user_repository,
            role_repository=self.role_repository,
            password_hasher=self.password_hasher,
        )
    
    
    @pytest.mark.anyio
    async def test_register_user_default(
        self
    ) -> None:
                
        service = AuthService(
            user_repository=self.user_repository,
            password_hasher=self.password_hasher,
            role_repository=self.role_repository    
        )
        
        payload = RegisterRequest(
            name = "Victor Ramos",
            email = "victor@email.com",
            password = "password1234"
        )
        
       
        result = await service.register(payload)
        
        assert result.id is not None
    
    
    @pytest.mark.anyio
    async def test_implemente_role_in_user_success(
        self,
        add_roles,
        add_user
    ) -> None:
        await self.service.roles_implements(
            UserRequestRole(
                id = 1,
                roles=[1, 4, 2]
            )
        )
        
        
        retorno = await self.service.get_by_id(
            user_id=1
        )
        
        assert retorno is not None
        assert retorno.roles == [1, 2]
        

    
    @pytest.mark.anyio
    async def test_delete_role_on_user(
        self,
        add_roles,
        add_user
    ) -> None:
        
        await self.service.roles_implements(
            UserRequestRole(
                id = 1,
                roles=[1, 4, 2]
            )
        )
        
        response_delete = await self.service.role_delete(
            user_id=1,
            role_id=2
        )

        assert response_delete is not None
        assert len(response_delete.roles) == 1