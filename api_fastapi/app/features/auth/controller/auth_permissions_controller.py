from fastapi import APIRouter, Depends, status
from app.features.auth.schemas.auth_permission_schema import PermissionRequest
from app.features.auth.dependencies import PermissionServiceDep

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