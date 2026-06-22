from app.features.auth.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

from app.features.auth.exceptions.services_erros import EmailAlreadyExistsError
from app.features.auth.entities.user_entity import User

class AuthService:
    
    def __init__(self, user_repository, password_hasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        
        
    async def register(self, payload: RegisterRequest) -> UserResponse:
        existing_user = self.user_repository.get_by_email(payload.email)
        
        
        if existing_user:
            raise EmailAlreadyExistsError("Email já registrado")

        password_hash = self.password_hasher.hash(payload.password)
        
        user = User(
            id=None,
            name=payload.name,
            email=payload.email,
            password_hash=password_hash,
        )
        created_user = self.user_repository.create(user)

        return UserResponse(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
            is_active=created_user.is_active,
        )

    async def login(self, payload: LoginRequest) -> TokenResponse:
        # Implement login logic here
        return TokenResponse(access_token="fake-token", token_type="bearer")