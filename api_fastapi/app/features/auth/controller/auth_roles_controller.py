from fastapi import APIRouter, status
from app.features.auth.schemas.auth_roles_schema import RolesRequest
from app.features.auth.dependencies.roles_dependencies import RolesServiceDep

router = APIRouter()

@router.post(
    "/roles",
    status_code=status.HTTP_201_CREATED,
)
async def post_roles(
    payload: RolesRequest,
    service: RolesServiceDep  
):
    return await service.create_roles(payload)

@router.get(
    "/roles",
    status_code = status.HTTP_200_OK
)
async def list_roles(
    service: RolesServiceDep
):
    return await service.list_roles()