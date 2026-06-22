
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session
from app.features.auth.security.password_hasher import PasswordHasher

from app.features.auth.repository.user_repository import UserRepository


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserRepository:
    return UserRepository(session=session)


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> UserRepository:
    from app.features.auth.service.auth_service import AuthService
    return AuthService(user_repository=user_repository, password_hasher=password_hasher)