from fastapi import APIRouter, Depends, status
from app.features.auth.dependencies import get_auth_service
from app.features.auth.schemas.auth_schema import (
    LoginRequest, 
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

from app.features.auth.service.auth_service import AuthService

router = APIRouter()

@router.post(
    "/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    return service.register(payload)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return service.login(payload)