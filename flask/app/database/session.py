from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

CONNECTION_URL = "sqlite+aiosqlite:////tmp/notes.db"


async_session_factory: async_sessionmaker = None


def init_db(url: str):
    global async_session_factory
    async_session_factory = async_sessionmaker(bind=create_async_engine(url))


def get_session() -> AsyncSession:
    return async_session_factory()
