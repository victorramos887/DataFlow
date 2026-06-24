
from app.features.auth.schemas.auth_roles_schema import RolesRequest
from app.features.auth.exceptions.services_erros import RoleAlreadyExistisError
from app.features.auth.entities.roles_entity import Role
from app.features.auth.schemas.auth_roles_schema import RolesResponse
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
        
    