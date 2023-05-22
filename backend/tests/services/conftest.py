import pytest
from app.database import Base, async_session, engine
from sqlalchemy import delete


@pytest.fixture(scope="session")
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db(create_db):
    async with async_session() as session:
        yield session

        for name, table in Base.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()
