from typing import Annotated
from fastapi import Depends
from app.core.dependencies import SessionDep

from app.features.auth.service.auth_permission_service import PermissionService
from app.features.auth.repository.permission_repository import PermissionRepository

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