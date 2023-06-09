import pytest
from app.config import settings
from app.database import Base
from app.main import app
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def postgres_container():
    postgres = PostgresContainer(
        image="postgres:15.2",
        user=settings.postgres_user,
        password=settings.postgres_password,
        dbname=settings.postgres_db + "_test",
        port=settings.postgres_port,
    )

    with postgres:
        wait_for_logs(
            postgres,
            r"UTC \[1\] LOG:  database system is ready to accept connections",
            10,
        )
        postgres.driver = "asyncpg"
        yield postgres


@pytest.fixture(scope="session")
async def db_engine(postgres_container):
    engine = create_async_engine(postgres_container.get_connection_url())
    yield engine


@pytest.fixture(scope="session")
async def db_session(db_engine):
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    yield async_session


@pytest.fixture
async def db(db_session, db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Just in case.
        await conn.run_sync(Base.metadata.create_all)

    async with db_session() as session:
        yield session

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
