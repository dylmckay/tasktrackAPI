from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from app.db import get_db
from app.main import app
from app.models.task import Base


@pytest.fixture(scope="session")
def pg_container() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:17") as pg:
        yield pg


@pytest_asyncio.fixture(scope="session")
async def db_engine(pg_container: PostgresContainer) -> AsyncGenerator[AsyncEngine]:
    url = pg_container.get_connection_url(driver="asyncpg")
    engine = create_async_engine(url)

    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    async with db_engine.connect() as connection:
        transaction = await connection.begin()
        session_maker = async_sessionmaker()
        session = session_maker(
            bind=connection, join_transaction_mode="create_savepoint"
        )
        yield session
        await transaction.rollback()


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
        app.dependency_overrides.clear()
