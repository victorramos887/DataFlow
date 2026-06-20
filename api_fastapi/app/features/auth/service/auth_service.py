from app.features.auth.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


class AuthService:
    def register(self, payload: RegisterRequest) -> UserResponse:
        # Implement registration logic here
        return UserResponse(id=1, name=payload.name, email=payload.email, is_active=True)

    def login(self, payload: LoginRequest) -> TokenResponse:
        # Implement login logic here
        return TokenResponse(access_token="fake-token", token_type="bearer")