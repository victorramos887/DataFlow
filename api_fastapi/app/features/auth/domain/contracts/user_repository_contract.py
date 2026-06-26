from typing import Protocol
from app.features.auth.domain.entities.user_entity import User


class UserRepositoryContract(Protocol):
    async def get_by_email(self, email: str) -> User | None:
        ...
        
    async def create(self, user: User) -> User:
        ...
        
    async def get_by_id(self, id: int) -> User | None:
        ...
    
    async def assing_roles(self, user_id: int, role_ids: list[int]) -> User | None:
        ...
        
    async def delete_roles(self, user_id: int, role_id: int) -> User | None:
        ...