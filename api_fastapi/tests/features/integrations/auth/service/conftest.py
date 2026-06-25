import os
import pytest

from app.features.auth.models.role_model import RoleModel
from app.features.auth.models.user_model import UserModel
from app.features.auth.schemas.auth_schema import RegisterRequest
from app.features.auth.models.permission_model import PermissionModel


@pytest.fixture
async def add_roles(async_session):
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

        async_session.add(role_)
    await async_session.commit()
    
@pytest.fixture
async def add_user(async_session):
    
    users = [
        {"id":1, "name":"Usuários 01", "email":"usuariofisrt@gmail.com", "password":"password1234"},
        {"id":2, "name":"Usuários 02", "email":"usuario2@gmail.com", "password":"password1234"},
        {"id":3, "name":"Usuários 03", "email":"usuario3@gmail.com", "password":"password1234"},
        {"id":4, "name":"Usuários 04", "email":"usuario4@gmail.com", "password":"password1234"}
    ]
    
    for user in users:
        user_ = UserModel(
            id=user.get("id"),
            email=user.get("email"),
            name=user.get("name"),
            password_hash=user.get("password")
        )
        
        async_session.add(user_)
    await async_session.commit()
    
@pytest.fixture
async def add_permission(async_session):
    permissions = [
        # Users / API
        {"id": 1, "name": "users:read", "description": "Listar usuários"},
        {"id": 2, "name": "users:read_by_id", "description": "Buscar usuário por ID"},
        {"id": 3, "name": "users:create", "description": "Criar usuário"},
        {"id": 4, "name": "users:update", "description": "Atualizar usuário"},
        {"id": 5, "name": "users:delete", "description": "Deletar usuário"},

        # Roles / API
        {"id": 6, "name": "roles:read", "description": "Listar cargos"},
        {"id": 7, "name": "roles:create", "description": "Criar cargo"},
        {"id": 8, "name": "roles:update", "description": "Atualizar cargo"},
        {"id": 9, "name": "roles:delete", "description": "Deletar cargo"},

        # Permissions / API
        {"id": 10, "name": "permissions:read", "description": "Listar permissões"},
        {"id": 11, "name": "permissions:create", "description": "Criar permissão"},
        {"id": 12, "name": "permissions:update", "description": "Atualizar permissão"},
        {"id": 13, "name": "permissions:delete", "description": "Deletar permissão"},

        # Telas / Frontend
        {"id": 14, "name": "screen:dashboard:view", "description": "Acessar dashboard"},
        {"id": 15, "name": "screen:users:view", "description": "Acessar tela de usuários"},
        {"id": 16, "name": "screen:roles:view", "description": "Acessar tela de cargos"},
        {"id": 17, "name": "screen:admin:view", "description": "Acessar área administrativa"},
    ]
    
    for permission in permissions:
        permissions_ = PermissionModel(
            id=permission.get("id"),
            name=permission.get("name"),
            description=permission.get("description")
        )
        
        async_session.add(permissions_)
        
    await async_session.commit()
        