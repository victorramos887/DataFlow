from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession



async def get_async_session():
    from app.core.database import async_session
    async with async_session() as session:
        yield session
    
