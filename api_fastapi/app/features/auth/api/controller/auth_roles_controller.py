from fastapi import APIRouter, status, Depends
from app.features.auth.api.schemas.auth_roles_schema import RolesRequest, RolesPermission
from app.features.auth.api.dependencies.roles_dependencies import RolesServiceDep

from app.features.auth.api.dependencies.authorization_dependencies import get_current_user, require_permission

protected_router = APIRouter(
    prefix="/roles",
    dependencies=[Depends(get_current_user)],
)

public_router = APIRouter(
    prefix="/auth",
)


@protected_router.post(
    "/register",
    dependencies=[Depends(require_permission("roles.create"))],
    status_code=status.HTTP_201_CREATED,
)
async def post_roles(
    payload: RolesRequest,
    service: RolesServiceDep  
):
    return await service.create_roles(payload)

@protected_router.get(
    "/",
    dependencies=[Depends(require_permission("roles.read"))],
    status_code = status.HTTP_200_OK
)
async def list_roles(
    service: RolesServiceDep
):
    return await service.list_roles()

@protected_router.patch(
    "/permission",
    status_code = status.HTTP_200_OK
)
async def patch_permission_in_role(
    payload: RolesPermission,
    service: RolesServiceDep
):
    return await service.permission_implements(payload)
