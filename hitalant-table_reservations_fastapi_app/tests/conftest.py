from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import orm_settings


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with orm_settings.get_session() as session:
        yield session
