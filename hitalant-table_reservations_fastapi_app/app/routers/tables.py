from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tables_crud import (
    get_by_name_table_or_none,
    create_table,
    delete_table,
    get_list_tables,
)
from app.db.database import orm_settings
from app.schemas.tables_schema import (
    TableCreateSchema,
    TableReadSchema,
)

router_tables = APIRouter(prefix="/api/v1/tables", tags=["tables"])


@router_tables.get(
    '/',
    response_model=list[TableReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_tables_router(
    session: AsyncSession = Depends(orm_settings.get_session)
):

    return await get_list_tables(session)


@router_tables.post(
    '/',
    response_model=TableReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_new_table_router(
    table: TableCreateSchema,
    session: AsyncSession = Depends(orm_settings.get_session),
):

    if await get_by_name_table_or_none(table.name, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Название стола "{table.name}" уже существует.'
        )

    return await create_table(table, session)


@router_tables.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_table_router(
    id: int,
    session: AsyncSession = Depends(orm_settings.get_session)
):
    deleted_table_count = await delete_table(id, session)
    if deleted_table_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Стола с id = {id} не существует.'
        )
