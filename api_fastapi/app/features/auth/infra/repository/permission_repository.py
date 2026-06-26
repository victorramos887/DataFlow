from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from app.features.auth.domain.entities.permission_entity import Permission
from app.features.auth.domain.entities.roles_entity import Role
from app.features.auth.infra.models.permission_model import PermissionModel

from app.features.auth.infra.models.user_model import UserModel
from app.features.auth.infra.models.role_model import RoleModel
class PermissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, permission: Permission) -> Permission:
        permission_model = PermissionModel(
            name = permission.name,
            description = permission.description,
            roles = []
        )

        self.session.add(permission_model)
        await self.session.commit()
        await self.session.refresh(permission_model)

        return Permission(
            id=permission_model.id,
            name=permission_model.name,
            description=permission_model.description,
        )
        
    async def get_by_name(self, name: str) -> Permission | None:
        result = await self.session.execute(
            select(PermissionModel).where(PermissionModel.name == name)
        )
        permission_model = result.scalars().first()

        if not permission_model:
            return None

        return Permission(
            id=permission_model.id,
            name=permission_model.name,
            description=permission_model.description,
        )
        
    async def list_permissions(self) -> list[Permission]:
        result = await self.session.execute(
            select(PermissionModel)
            .options(selectinload(PermissionModel.roles))
        )
        permission_models = result.scalars().all()

        return [
            Permission(
                id=permission_model.id,
                name=permission_model.name,
                description=permission_model.description,
                roles=[
                    Role(
                        id=role.id,
                        name=role.name,
                        description = role.description
                    ) for role in permission_model.roles
                ]
            )
            for permission_model in permission_models
        ]
    
    async def get_by_id(self, permission_id: int) -> Permission | None:
        result = await self.session.execute(
            select(PermissionModel).where(PermissionModel.id == permission_id)
        )
        permission_model = result.scalars().first()

        if not permission_model:
            return None

        return Permission(
            id=permission_model.id,
            name=permission_model.name,
            description=permission_model.description,
        )
        
    async def user_has_permission(
        self,
        user_id: int,
        permission_name: str,
    ) -> bool:
        stmt = (
            select(PermissionModel.id)
            .join(PermissionModel.roles)
            .join(RoleModel.users)
            .where(
                UserModel.id == user_id,
                PermissionModel.name == permission_name,
            )
            .limit(1)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None