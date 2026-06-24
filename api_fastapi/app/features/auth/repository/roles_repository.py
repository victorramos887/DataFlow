from sqlalchemy.ext.asyncio import AsyncSession
from app.features.auth.entities.roles_entity import Roles

from app.features.auth.models.role_model import RoleModel

class RolesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(self, roles: Roles) -> Roles:
        role_model = RoleModel(
            name = roles.name,
            description = roles.description
        )
        
        self.session.add(role_model)
        await self.session.commit()
        await self.session.refresh(role_model)
        
        return Roles(
            id=role_model.id,
            name=role_model.name,
            description=role_model.description
        )
        