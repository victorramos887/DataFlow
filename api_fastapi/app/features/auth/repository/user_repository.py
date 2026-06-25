from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.features.auth.entities.roles_entity import Role
from app.features.auth.models.user_model import UserModel
from app.features.auth.models.role_model import RoleModel
from app.features.auth.entities.user_entity import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)

        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            is_active=user_model.is_active,
        )

    async def create(self, user: User) -> User:
        user_model = UserModel(
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
        )

        self.session.add(user_model)

        await self.session.commit()
        await self.session.refresh(user_model)

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            is_active=user_model.is_active,
        )
        
    async def get_by_id(self, id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.id == id)
        
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if user_model is None:
            return None

        return  User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            is_active=user_model.is_active,
            roles=user_model.roles
        )

    async def assign_roles(self, user_id: int, role_ids: list[int]) -> User | None:
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.id == user_id)
        )
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        current_role_ids = {role.id for role in user_model.roles}
        new_role_ids = [rid for rid in dict.fromkeys(role_ids) if rid not in current_role_ids]

        if new_role_ids:
            role_result = await self.session.execute(
                select(RoleModel).where(RoleModel.id.in_(new_role_ids))
            )
            user_model.roles.extend(role_result.scalars().all())
            await self.session.commit()

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            is_active=user_model.is_active,
            roles=[Role(id=r.id, name=r.name, description=r.description) for r in user_model.roles],
        )
        
    async def delete_roles(self, user_id: int, role_id: int) -> User | None:
        
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.id == user_id)
        )
            
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        if user_model is None:
            return None
        
        role_to_remove = next(
            (role for role in user_model.roles if role.id == role_id),
            None,
        )

        if role_to_remove is None:
            return None

        user_model.roles.remove(role_to_remove)

        await self.session.commit()
        await self.session.refresh(user_model)

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            is_active=user_model.is_active,
            roles=[
                Role(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                )
                for role in user_model.roles
            ],
        )
            
        