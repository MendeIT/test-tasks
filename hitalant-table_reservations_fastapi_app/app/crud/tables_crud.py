from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Table
from app.schemas.tables_schema import TableCreateSchema


async def create_table(
    data: TableCreateSchema,
    session: AsyncSession
) -> Table:
    """Создание стола."""

    table = Table(**data.model_dump())
    session.add(table)
    await session.commit()
    await session.refresh(table)

    return table


async def get_list_tables(session: AsyncSession) -> list[Table]:
    """Получить список столов."""

    query = select(Table)
    result = await session.execute(query)

    return result.scalars().all()


async def delete_table(
    table_id: int,
    session: AsyncSession
) -> int:
    """Удалить стол. Возвращает кол-во удалённых записей."""

    query = delete(Table).where(
        Table.table_id == table_id
    )
    result = await session.execute(query)
    await session.commit()

    return result.rowcount


async def get_by_name_table_or_none(
    table_name: str,
    session: AsyncSession
) -> bool:
    """Проверяет, существует ли стол с указанным id."""

    query = select(Table).where(Table.name == table_name)
    result = await session.execute(query)

    return result.scalar_one_or_none()
