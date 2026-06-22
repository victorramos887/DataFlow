
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session
from app.features.auth.security.password_hasher import PasswordHasher

from app.features.auth.repository.user_repository import UserRepository
from app.features.auth.service.auth_permission_service import PermissionService
from app.features.auth.repository.permission_repository import PermissionRepository
from app.features.auth.service.auth_service import AuthService

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

async def get_user_repository(
    session: SessionDep) -> UserRepository:
    return UserRepository(session=session)

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


AuthRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
PasswordHasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]

def get_auth_service(
    user_repository: AuthRepositoryDep,
    password_hasher: PasswordHasherDep,
) -> UserRepository:
    from app.features.auth.service.auth_service import AuthService
    return AuthService(user_repository=user_repository, password_hasher=password_hasher)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

def get_permission_repository(
    session: SessionDep,
) -> PermissionRepository:
    return PermissionRepository(session=session)


PermissionRepositoryDep = Annotated[
    PermissionRepository,
    Depends(get_permission_repository),
]


def get_permission_service(
    permission_repository: PermissionRepositoryDep,
) -> PermissionService:
    return PermissionService(permission_repository=permission_repository)


PermissionServiceDep = Annotated[
    PermissionService,
    Depends(get_permission_service),
]