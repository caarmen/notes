from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from app.database.model import Base
from app.database.session import get_session
from app.main import app
from tests.factories import NoteFactory

# Factories use a sync db session via pytest-sqlalchemy-mock
# https://github.com/resulyrt93/pytest-sqlalchemy-mock
# Our app, however, uses an async session.
# Set up a test database in a temporary file. Make factories use
# the sync db session, and the app use an async session, on this
# same database file.


# Configure a temporary db file, which will be used for both the sync and async sessions
@pytest.fixture
def tmp_db_file(tmp_path):
    return tmp_path / "test.db"


#### Sync session for factories ####


# Tell pytest-sqlalchemy-mock where to find our db model:
@pytest.fixture
def sqlalchemy_declarative_base():
    return Base


# Set a connection url to the db, for the pytest-sqlalchemy-mock sync session
@pytest.fixture
def connection_url(tmp_db_file):
    return f"sqlite:///{tmp_db_file}"


# Configure factories to use the pytest-sqlalchemy-mock session
@pytest.fixture(scope="function", autouse=True)
def setup_factories(mocked_session: Session):
    NoteFactory._meta.sqlalchemy_session = mocked_session


#### Async session for the app and test assertions ####


# Configure a mocked async session for our tests to use.
@pytest_asyncio.fixture
async def mocked_async_session(tmp_db_file: str) -> AsyncGenerator[AsyncSession, None]:
    async_connection_url = f"sqlite+aiosqlite:///{tmp_db_file}"
    # https://peps.python.org/pep-0525/#asynchronous-yield-from
    async for session in get_session(url=async_connection_url):
        yield session


# Configure our app to use the async session
@pytest.fixture
def client(mocked_async_session) -> TestClient:
    app.dependency_overrides[get_session] = lambda: mocked_async_session
    return TestClient(app)
