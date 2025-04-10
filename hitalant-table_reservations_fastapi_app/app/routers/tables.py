from fastapi import APIRouter

router_tables = APIRouter(prefix="/api/v1/tables")


@router_tables.get('')
async def get_tables():
    return {'success': 'много столов!'}


@router_tables.post('')
async def create_tables():
    return {'success': 'Новый стол создан!'}


@router_tables.delete('{id}')
async def delete_table(id):
    return {'success': id + 'удален стол!'}
