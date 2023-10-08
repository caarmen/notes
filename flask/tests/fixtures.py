from pathlib import Path

import pytest
import pytest_asyncio
from flask.testing import FlaskClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from app.database.model import Base
from app.database.session import get_session
from app.main import AppConfig, create_app
from flask import Flask
from tests.factories import NoteFactory

# Factories use a sync db session via pytest-sqlalchemy-mock
# https://github.com/resulyrt93/pytest-sqlalchemy-mock
# Our app, however, uses an async session.
# Set up a test database in a temporary file. Make factories use
# the sync db session, and the app use an async session, on this
# same database file.


# Configure a temporary db file, which will be used for both the sync and async sessions
@pytest.fixture
def tmp_db_file(tmp_path) -> Path:
    return tmp_path / "test.db"


#### Sync session for factories ####


# Tell pytest-sqlalchemy-mock where to find our db model:
@pytest.fixture
def sqlalchemy_declarative_base():
    return Base


# Set a connection url to the db, for the pytest-sqlalchemy-mock sync session
@pytest.fixture
def connection_url(tmp_db_file: Path) -> str:
    return f"sqlite:///{tmp_db_file}"


# Configure factories to use the pytest-sqlalchemy-mock session
@pytest.fixture(scope="function", autouse=True)
def setup_factories(mocked_session: Session):
    NoteFactory._meta.sqlalchemy_session = mocked_session


#### Async session for the app and test assertions ####


# Configure a mocked async session for our tests to use.
@pytest_asyncio.fixture
async def mocked_async_session() -> AsyncSession:
    async with get_session() as session:
        yield session


@pytest.fixture()
def app(tmp_db_file) -> Flask:
    async_connection_url = f"sqlite+aiosqlite:///{tmp_db_file}"
    app = create_app(config=AppConfig(db_connection_url=async_connection_url))
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
