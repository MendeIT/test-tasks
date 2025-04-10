from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.core.config import settings
from app.db.models import Base


class OrmSettgings:
    """Настройки SQLAlchemy."""

    def __init__(self):
        self.async_engine = create_async_engine(
            url=settings.ASYNC_DATABASE_URL,
            execution_options={"options": f"-c timezone={settings.TIMEZONE}"},
            echo=settings.DEBUG,
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Подключение к базе данных."""
        async with self.async_session_maker() as session:
            yield session

    async def shutdown_session(self) -> None:
        """Закрытие соединения с базой данных."""
        await self.async_engine.dispose()

    async def _init_models(self) -> None:
        """Создание таблиц базы данных."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _drop_models(self) -> None:
        """Удаление всех таблиц."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


orm_settings = OrmSettgings()
