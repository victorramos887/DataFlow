from app.features.auth.schemas.auth_permission_schema import PermissionRequest
from app.features.auth.exceptions.services_erros import PermissionAlreadyExistsError
from app.features.auth.entities.permission_entity import Permission
from app.features.auth.schemas.auth_permission_schema import PermissionResponse
class PermissionService:
    def __init__(self, permission_repository) -> None:
        self.permission_repository = permission_repository

    async def create_permission(self, payload: PermissionRequest):
        existing_permission = await self.permission_repository.get_by_name(payload.name)
        
        if existing_permission:
            return PermissionAlreadyExistsError("Permission already exists")
        
        permission = Permission(
            id=None,
            name=payload.name,
            description=payload.description,
        )
        created_permission = await self.permission_repository.create(permission)
        
        return PermissionResponse(
            id=created_permission.id,
            name=created_permission.name,
            description=created_permission.description,
        )
    
    async def list_permissions(self):
        permissions = await self.permission_repository.list_permissions()
        return [
            PermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
            )
            for permission in permissions
        ]
    
    async def get_permission(self, permission_id: int):
        permission = await self.permission_repository.get_by_id(permission_id)
        if not permission:
            return None
        
        return PermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
        )