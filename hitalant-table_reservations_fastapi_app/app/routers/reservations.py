from fastapi import APIRouter

router_reservations = APIRouter(prefix="/api/v1/reservations")


@router_reservations.get('')
async def get_reservations():
    return {'success': 'много броней столов!'}


@router_reservations.post('')
async def create_reservations():
    return {'success': 'Новая бронь стола создана!'}


@router_reservations.delete('{id}')
async def delete_reservations(id):
    return {'success': id + 'бронь стола удалена!'}
