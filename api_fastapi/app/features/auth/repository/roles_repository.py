from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.features.auth.entities.roles_entity import Role
from app.features.auth.entities.permission_entity import Permission

from app.features.auth.models.role_model import RoleModel
from app.features.auth.models.permission_model import PermissionModel

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
        
    async def get_by_id(self, role_id: int) -> Role | None:
        result = await self.session.execute(
            select(RoleModel).where(RoleModel.id == role_id)
        )
        
        role_model = result.scalar_one_or_none()
        
        if not role_model:
            return None
        
        return Role(
            id=role_model.id,
            name = role_model.name,
            description=role_model.description
        )
    
    async def list_roles(self) -> list[Role]:
        result = await self.session.execute(
            select(RoleModel)
            .options(selectinload(RoleModel.permission))
        )
        role_models = result.scalars().all()
        return [
            Role(
                id=role_model.id,
                name=role_model.name,
                description=role_model.description,
                permission=[
                    Permission(
                        id=permission.id,
                        name=permission.name,
                        description=permission.description
                    )
                    for permission in role_model.permission
                ]
            )
            for role_model in role_models
        ]
        
    async def assign_permission(self, roles_id: int, permission_ids: list[int]) -> Role | None:
        
        stmt = (
            select(RoleModel)
            .options(selectinload(RoleModel.permission))
            .where(RoleModel.id == roles_id)
        )
        
        result = await self.session.execute(stmt)
        role_model = result.scalar_one_or_none()
        
        if role_model is None:
            return None
        
        current_permission_ids = {permission.id for permission in role_model.permission}
        new_permission_id = [pid for pid in dict.fromkeys(permission_ids) if pid not in current_permission_ids]
        
        if new_permission_id:
            permission_result = await self.session.execute(
                select(PermissionModel).where(PermissionModel.id.in_(new_permission_id))
            )
            role_model.permission.extend(permission_result.scalars().all())
        
            await self.session.commit()
            
        return Role(
            id=role_model.id,
            name=role_model.name,
            description=role_model.description,
            permission=[Permission(id=p.id, name=p.name, description=p.description) for p in role_model.permission]
        )