from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

CONNECTION_URL = "sqlite+aiosqlite:////tmp/notes.db"


async def get_session(url: str = CONNECTION_URL) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = async_sessionmaker(bind=create_async_engine(url))()
    try:
        yield session
    finally:
        await session.close()
