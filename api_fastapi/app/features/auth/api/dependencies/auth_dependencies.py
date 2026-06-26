from typing import Annotated
from fastapi import Depends
from app.core.dependencies import SessionDep
from app.features.auth.infra.security.password_hasher import PasswordHasher

from app.features.auth.infra.repository.user_repository import UserRepository

from app.features.auth.application.service.auth_service import AuthService
from app.features.auth.api.dependencies.roles_dependencies import RolesRepositoryDep
from fastapi.security import OAuth2PasswordRequestForm


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
    role_repository: RolesRepositoryDep
) -> AuthService:
    return AuthService(user_repository=user_repository, role_repository=role_repository, password_hasher=password_hasher)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


AuthOAuthDep = Annotated[OAuth2PasswordRequestForm, Depends()]