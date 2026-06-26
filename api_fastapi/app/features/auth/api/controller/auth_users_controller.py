from fastapi import APIRouter, Depends, status, HTTPException
from app.features.auth.api.dependencies.auth_dependencies import get_auth_service
from app.features.auth.api.schemas.auth_schema import (
    LoginRequest, 
    RegisterRequest,
    UserRequestRole,
    TokenResponse,
    UserResponse,
)

from app.core.security import create_access_token
from app.features.auth.api.dependencies.auth_dependencies import AuthServiceDep, AuthOAuthDep
from app.features.auth.api.dependencies.authorization_dependencies import CurrentUserDep

router = APIRouter(prefix="/user")



@router.get("/me")
async def me(
    current_user: CurrentUserDep,
):
    return current_user

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
    form_data: AuthOAuthDep,
    service: AuthServiceDep
) -> TokenResponse:
    
    user = await service.authenticate(
        email=form_data.username,
        password=form_data.password
    )
    
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token = create_access_token(subject=str(user.id))
    
    return TokenResponse(
        access_token=token
    )


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