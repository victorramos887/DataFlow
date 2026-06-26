from typing import Annotated
from fastapi import Depends
from app.core.dependencies import SessionDep

from app.features.auth.application.service.auth_roles_service import RolesService
from app.features.auth.infra.repository.roles_repository import RolesRepository

def get_roles_repository(
    session: SessionDep
) -> RolesRepository:
    return RolesRepository(session=session)

RolesRepositoryDep = Annotated[
    RolesRepository,
    Depends(get_roles_repository)
]

def get_roles_service(
    roles_repository: RolesRepositoryDep,
) -> RolesService:
    return RolesService(roles_repository=roles_repository)

RolesServiceDep = Annotated[
    RolesService,
    Depends(get_roles_service)
]