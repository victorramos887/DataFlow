from sqlalchemy.ext.asyncio import AsyncSession
from app.features.auth.entities.roles_entity import Roles



class RolesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(self, roles: Roles) -> Roles:
        pass
        