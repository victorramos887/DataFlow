from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.models.user_model import UserModel
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