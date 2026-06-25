import pytest

from app.features.auth.schemas.auth_schema import RegisterRequest
from app.features.auth.service.auth_service import AuthService

from app.features.auth.repository.user_repository import UserRepository
from app.features.auth.repository.roles_repository import RolesRepository
from app.features.auth.security.password_hasher import PasswordHasher
from app.features.auth.models.role_model import RoleModel
from app.features.auth.models.user_model import UserModel

from sqlalchemy import select

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
    
    
    async def add_roles(self):
        roles = [
            {"id": 1, "name":"tecnica", "description":"Equipe ténica"}, 
            {"id": 2, "name":"cadastro", "description":"Cadastro ténico"},
            {"id": 3, "name":"admin", "description":"Administracao"}
        ]
        
        for role in roles:
            role_ = RoleModel(
                id=role.get("id"),
                name=role.get("name"),
                description=role.get("description")
            )

            self.async_session.add(role_)
        await self.async_session.commit()
    
    async def add_user(self):
        users = [
            RegisterRequest(name="Usuários 01", email="usuariofisrt@gmail.com", password="password1234"),
            RegisterRequest(name="Usuários 02", email="usuariosecond@gmail.com", password="password1234"),
        ]
        # Registra os dois: users[0] → id=1, users[1] → id=2
        await self.service.register(users[0])
        await self.service.register(users[1])
        
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
    ) -> None:
        
        await self.add_user()
        await self.add_roles()
        
        
        response_ = self.auth_client.patch(
            "/auth/roles",
            json={
                "id":2,
                "roles": [1, 4, 2]
            }
        )       
        
        assert response_.status_code == 201
        
        assert response_.json() == {
            "id": 2,
            "name": "Usuários 02",
            "email": "usuariosecond@gmail.com",
            "roles":[1, 2],
            "is_active": True,
        }
        response = self.auth_client.patch(
            "/auth/roles",
            json={
                "id":2,
                "roles": [1]
            }
        )
        assert response.json() == {
            "id": 2,
            "name": "Usuários 02",
            "email": "usuariosecond@gmail.com",
            "roles":[1, 2],
            "is_active": True,
        }
        
        assert 1 == 1
    
    @pytest.mark.anyio
    async def test_delete_role_on_user(
        self
    ) -> None:
        await self.add_user()
        await self.add_roles()
        
        response = self.auth_client.patch(
            "/auth/roles",
            json={
                "id":1,
                "roles": [1, 2]
            }
        )
        
        assert response.status_code == 201
        
        response_delete = self.auth_client.delete(
            f"/auth/roles/delete/{1}/{2}"
        )
       
        assert response_delete.status_code == 200
        assert response_delete.json() == {
            "id": 1,
            "name": "Usuários 01",
            "email": "usuariofisrt@gmail.com",
            "roles":[{'id': 1, 'name': 'tecnica', 'description': 'Equipe ténica'}],
            "is_active": True,
        }
        
        