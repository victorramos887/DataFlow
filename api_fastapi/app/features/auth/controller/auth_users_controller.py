from fastapi import APIRouter, Depends, status
from app.features.auth.dependencies.auth_dependencies import get_auth_service
from app.features.auth.schemas.auth_schema import (
    LoginRequest, 
    RegisterRequest,
    UserRequestRole,
    TokenResponse,
    UserResponse,
)

from app.features.auth.dependencies.auth_dependencies import AuthServiceDep

router = APIRouter(prefix="/user")

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


@router.patch(
    "/roles",
    response_model=UserResponse,
    status_code = status.HTTP_201_CREATED
)
async def roles_implement(
    payload: UserRequestRole,
    service: AuthServiceDep
) -> UserResponse:
    return await service.roles_implements(payload)

@router.delete(
    "/roles/delete/{user_id}/{role_id}",
    response_model=UserResponse,
    status_code = status.HTTP_200_OK
)
async def roles_delete(
    user_id: int,
    role_id: int,
    service: AuthServiceDep,
) -> UserResponse:
    return await service.role_delete(user_id=user_id, role_id=role_id)