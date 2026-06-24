from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.auth.entities.roles_entity import Role

from app.features.auth.models.role_model import RoleModel

class RolesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(self, roles: Role) -> Role:
        role_model = RoleModel(
            name = roles.name,
            description = roles.description
        )
        
        self.session.add(role_model)
        await self.session.commit()
        await self.session.refresh(role_model)
        
        return Role(
            id=role_model.id,
            name=role_model.name,
            description=role_model.description
        )
        
    async def get_by_name(self, role_name: str) -> Role | None:
        result = await self.session.execute(
            select(RoleModel).where(RoleModel.name == role_name)
        )
        
        role_model = result.scalars().first()
        
        if not role_model:
            return None
        
        return Role(
            id=role_model.id,
            name=role_model.name,
            description=role_model.description
        )
    
    async def list_roles(self) -> list[Role]:
        result = await self.session.execute(
            select(RoleModel)
        )
        role_models = result.scalars().all()
        
        return [
            Role(
                id=role_model.id,
                name=role_model.name,
                description=role_model.description
            )
            for role_model in role_models
        ]
        