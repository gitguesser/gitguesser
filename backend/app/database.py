from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    settings.database_url, echo=True
)  # Maybe change echo to False in the future.
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.drop_all
        )  # Can be commented in future if we want to preserve data in database.
        await conn.run_sync(Base.metadata.create_all)
