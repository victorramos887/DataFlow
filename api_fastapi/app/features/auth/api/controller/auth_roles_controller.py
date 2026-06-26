from fastapi import APIRouter, status
from app.features.auth.api.schemas.auth_roles_schema import RolesRequest, RolesPermission
from app.features.auth.api.dependencies.roles_dependencies import RolesServiceDep

router = APIRouter(prefix="/roles")

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def post_roles(
    payload: RolesRequest,
    service: RolesServiceDep  
):
    return await service.create_roles(payload)

@router.get(
    "/",
    status_code = status.HTTP_200_OK
)
async def list_roles(
    service: RolesServiceDep
):
    return await service.list_roles()

@router.patch(
    "/permission",
    status_code = status.HTTP_200_OK
)
async def patch_permission_in_role(
    payload: RolesPermission,
    service: RolesServiceDep
):
    return await service.permission_implements(payload)
