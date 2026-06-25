from app.features.auth.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    UserRequestRole
)

from app.features.auth.exceptions.services_erros import EmailAlreadyExistsError
from app.features.auth.entities.user_entity import User

class AuthService:
    
    def __init__(self, user_repository, role_repository, password_hasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.role_repository = role_repository
        
        
    async def register(self, payload: RegisterRequest) -> UserResponse:
        existing_user = await self.user_repository.get_by_email(payload.email)
        
        
        if existing_user:
            raise EmailAlreadyExistsError("Email já registrado")

        password_hash = self.password_hasher.hash_password(payload.password)
        
        user = User(
            id=None,
            name=payload.name,
            email=payload.email,
            password_hash=password_hash,
        )
        created_user = await self.user_repository.create(user)

        return UserResponse(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
            is_active=created_user.is_active,
            roles=[],
        )

    async def roles_implements(self, payload: UserRequestRole) -> UserResponse | None:
        
        updated_user = await self.user_repository.assign_roles(payload.id, payload.roles)

        if updated_user is None:
            return None
        

        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            is_active=updated_user.is_active,
            roles=[role.id for role in updated_user.roles if role.id is not None],
        )
    
    async def login(self, payload: LoginRequest) -> TokenResponse:
        # Implement login logic here
        return TokenResponse(access_token="fake-token", token_type="bearer")