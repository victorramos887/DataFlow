from typing import List
from app.features.auth.api.schemas.auth_roles_schema import RolesRequest
from app.features.auth.domain.exceptions.services_erros import RoleAlreadyExistisError
from app.features.auth.domain.entities.roles_entity import Role
from app.features.auth.api.schemas.auth_roles_schema import RolesResponse, RolesPermission, UserSummaryResponse, PermissionSummaryResponse
class RolesService:
    def __init__(self, roles_repository) -> None:
        self.roles_repository = roles_repository
        
    async def create_roles(self, payload: RolesRequest):
        existing_roles = await self.roles_repository.get_by_name(payload.name)
        
        if existing_roles:
            return RoleAlreadyExistisError("Roles already exists")
        
        role = Role(
            id = None,
            name=payload.name,
            description=payload.description
        )
        
        create_roles = await self.roles_repository.create(role)
        
        return RolesResponse(
            id=create_roles.id,
            name=create_roles.name,
            description=create_roles.description
        )
        
        
    async def list_roles(self) -> list[RolesResponse]:
        list_roles = await self.roles_repository.list_roles()
        if not list_roles:
            return None
        return [
        RolesResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=[
                PermissionSummaryResponse(
                    id=permission.id,
                    name=permission.name,
                    description=permission.description,
                )
                for permission in role.permission
            ],
            users=[
                UserSummaryResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    is_active=user.is_active,
                )
                for user in role.users
            ],
        )
        for role in list_roles
    ]
    
    
    async def permission_implements(self, payload: RolesPermission) -> RolesResponse:
        updated_roles = await self.roles_repository.assign_permission(payload.id, payload.permission)
        
        if updated_roles is None:
            return None
        
        return RolesResponse(
                id=updated_roles.id,
                name=updated_roles.name,
                description=updated_roles.description,
                permissions=[
                    PermissionSummaryResponse(
                        id=permission.id,
                        name=permission.name,
                        description=permission.description,
                    )
                    for permission in updated_roles.permission
                ],
                users=[
                    UserSummaryResponse(
                        id=user.id,
                        name=user.name,
                        email=user.email,
                        is_active=user.is_active,
                    )
                    for user in updated_roles.users
                ],
            )
        