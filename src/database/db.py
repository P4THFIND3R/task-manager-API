from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with async_sessionmaker() as session:
        yield session
