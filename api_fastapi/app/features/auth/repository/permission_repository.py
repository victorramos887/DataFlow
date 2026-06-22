from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.features.auth.entities.permission_entity import Permission
from app.features.auth.models.permission_model import PermissionModel

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
        result = await self.session.execute(select(PermissionModel))
        permission_models = result.scalars().all()

        return [
            Permission(
                id=permission_model.id,
                name=permission_model.name,
                description=permission_model.description,
            )
            for permission_model in permission_models
        ]