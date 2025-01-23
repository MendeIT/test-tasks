import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from dotenv import load_dotenv

from database.models import Base

load_dotenv()

async_engine = create_async_engine(
    url=os.getenv("DATABASE_URL"),
    echo=True,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_models():
    """Создание базы данных.
    Создание таблиц (для разработки).
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models():
    """Удаление базы данных.
    Удаление таблиц (для разработки).
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncSession:
    """Подключение к БД."""
    async with async_session_maker() as session:
        yield session


async def shutdown() -> None:
    """Закрытие соединения с БД."""
    await async_engine.dispose()
