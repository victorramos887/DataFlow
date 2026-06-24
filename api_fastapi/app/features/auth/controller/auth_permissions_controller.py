from fastapi import APIRouter, Depends, status
from app.features.auth.schemas.auth_permission_schema import PermissionRequest
from app.features.auth.dependencies.permission_dependencies import PermissionServiceDep

router = APIRouter()

@router.post(
    "/permissions",
    status_code=status.HTTP_200_OK,
)
async def post_permission(
    payload: PermissionRequest,
    service: PermissionServiceDep
):
    return await service.create_permission(payload)

@router.get(
    "/permissions",
    status_code=status.HTTP_200_OK,
    response_model=list[PermissionRequest]
)
async def list_permissions(
    service: PermissionServiceDep
):
    return await service.list_permissions()

@router.get(
    "/permissions/{permission_id}",
    status_code=status.HTTP_200_OK,
)
async def get_permission(
    permission_id: int,
    service: PermissionServiceDep
):
    return await service.get_permission(permission_id)