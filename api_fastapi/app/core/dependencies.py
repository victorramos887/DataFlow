from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    from app.core.database import get_async_session as get_db_async_session

    async for session in get_db_async_session():
        yield session
    
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]