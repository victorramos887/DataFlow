from typing import Annotated
from fastapi import Depends
from app.core.dependencies import SessionDep
from app.features.auth.security.password_hasher import PasswordHasher

from app.features.auth.repository.user_repository import UserRepository
from app.features.auth.service.auth_service import AuthService

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
) -> AuthService:
    return AuthService(user_repository=user_repository, password_hasher=password_hasher)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
