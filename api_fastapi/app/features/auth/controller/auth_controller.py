from fastapi import APIRouter, Depends, status
from app.features.auth.dependencies import get_auth_service
from app.features.auth.schemas.auth_schema import (
    LoginRequest, 
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

from app.features.auth.dependencies import AuthServiceDep

router = APIRouter()

@router.post(
    "/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    payload: RegisterRequest,
    service: AuthServiceDep
) -> UserResponse:
    return await service.register(payload)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def login(
    payload: LoginRequest,
    service: AuthServiceDep
) -> TokenResponse:
    return await service.login(payload)


