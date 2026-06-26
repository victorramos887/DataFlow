from typing import Annotated

from fastapi import Depends, HTTPException, Security, status

from app.core.security import decode_access_token, oauth2_schema
from app.features.auth.api.dependencies.auth_dependencies import AuthRepositoryDep
from app.features.auth.api.dependencies.permission_dependencies import PermissionRepositoryDep
from app.features.auth.domain.entities.user_entity import User


TokenDep = Annotated[str, Security(oauth2_schema)]


async def get_current_user(
    token: TokenDep,
    user_repository: AuthRepositoryDep,
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await user_repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def require_permission(permission_name: str):
    async def dependency(
        current_user: CurrentUserDep,
        permission_repository: PermissionRepositoryDep,
    ) -> User:
        has_permission = await permission_repository.user_has_permission(
            user_id=current_user.id,
            permission_name=permission_name,
        )
        
        print(f"has_permission: {has_permission}")

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return dependency