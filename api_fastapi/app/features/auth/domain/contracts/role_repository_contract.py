from typing import Protocol
from app.features.auth.domain.entities.roles_entity import Role

class RolesRepositoryContract(Protocol):
    
    async def create(self, roles: Role) -> Role:
        ...
    
    async def get_by_name(self, role_name: str) -> Role | None:
        ...
    
    async def get_by_id(self, role_id: int) -> Role | None:
        ...
        
    async def list_roles(self) -> list[Role]:
        ...
        
    async def assign_permission(self, roles_id: int, permission_ids: list[int]) -> Role | None:
        ...