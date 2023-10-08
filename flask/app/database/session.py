import dataclasses

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

CONNECTION_URL = "sqlite+aiosqlite:////tmp/notes.db"


@dataclasses.dataclass
class DbConfig:
    async_session_factory: async_sessionmaker | None


db_config = DbConfig(async_session_factory=None)


def init_db(url: str = CONNECTION_URL):
    db_config.async_session_factory = async_sessionmaker(bind=create_async_engine(url))


def get_session() -> AsyncSession:
    return db_config.async_session_factory()
