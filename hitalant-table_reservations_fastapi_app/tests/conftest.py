import asyncio
from typing import Any, AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.core.config import settings
from app.core.register import register_routers
from app.db.models import Table, Reservation
from app.main import create_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_engine():
    """Фикстура для тестового асинхронного движка БД."""

    engine = create_async_engine(
        settings.ASYNC_DATABASE_URL,
        pool_size=10,
        max_overflow=5,
        pool_timeout=30,
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(db_engine):
    """Фикстура для асинхронной сессии."""

    async_session = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура тестового пользователя."""

    app = create_app()
    register_routers(app)

    async with AsyncClient(app=app, base_url='http://test_url') as client:
        yield client


@pytest.fixture
async def test_tables(session) -> list[dict[str, Any]]:
    """Фикстура для тестовых данных таблиц."""

    await session.execute(delete(Table))
    await session.execute(delete(Reservation))

    tables_data = [
        {
            "table_id": 1,
            "name": "Стол 1",
            "seats": 4,
            "location": "Терраса"
        },
        {
            "table_id": 2,
            "name": "Стол 2",
            "seats": 2,
            "location": "Барная стойка"
        }
    ]

    await session.execute(insert(Table).values(tables_data))
    await session.commit()

    return tables_data
