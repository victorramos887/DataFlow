from fastapi import APIRouter, Depends, status
from app.features.auth.api.schemas.auth_permission_schema import PermissionRequest, PermissionResponse
from app.features.auth.api.dependencies.permission_dependencies import PermissionServiceDep

from app.features.auth.api.dependencies.authorization_dependencies import require_permission

router = APIRouter(prefix="/permissions")

@router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("permissions.create"))]
)
async def post_permission(
    payload: PermissionRequest,
    service: PermissionServiceDep
):
    return await service.create_permission(payload)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PermissionResponse],
    dependencies=[Depends(require_permission("permissions.read"))]
)
async def list_permissions(
    service: PermissionServiceDep
):
    print("list_permissions called")
    return await service.list_permissions()

@router.get(
    "/{permission_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("permissions.read"))]
)
async def get_permission(
    permission_id: int,
    service: PermissionServiceDep
):
    return await service.get_permission(permission_id)