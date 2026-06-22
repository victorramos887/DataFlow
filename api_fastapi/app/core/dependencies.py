from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    from app.core.database import get_async_session as get_db_async_session

    async for session in get_db_async_session():
        yield session
    
