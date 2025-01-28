from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from core.conf import settings
from database.models import Base


# Для подключения Apscheduler
sync_engine = create_engine(
    url=settings.SYNC_DATABASE_URL,
    echo=settings.DEBUG
)

async_engine = create_async_engine(
    url=settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_models():
    """Создание таблиц (для разработки)."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models():
    """Удаление таблиц (для разработки)."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@asynccontextmanager
async def get_session() -> AsyncSession:
    """Подключение к БД."""
    async with async_session_maker() as session:
        yield session


async def shutdown() -> None:
    """Закрытие соединения с БД."""
    await async_engine.dispose()
