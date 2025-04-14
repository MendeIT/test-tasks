from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.reservations_crud import (
    get_reservations_by_table,
    create_reservation,
    delete_reservation,
    get_list_reservations,
    has_reservation_conflict,
)
from app.db.database import orm_settings
from app.schemas.reservations_schema import (
    ReservationCreateSchema,
    ReservationReadSchema,
)

router_reservations = APIRouter(
    prefix="/api/v1/reservations", tags=["reservations"]
)


@router_reservations.get(
    '/',
    response_model=list[ReservationReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_list_reservations_router(
    session: AsyncSession = Depends(orm_settings.get_session)
):
    return await get_list_reservations(session)


@router_reservations.post(
    '/',
    response_model=ReservationReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_new_reservation_router(
    reservation: ReservationCreateSchema,
    session: AsyncSession = Depends(orm_settings.get_session)
):
    existing_reservations = await get_reservations_by_table(
        reservation,
        session
    )
    if has_reservation_conflict(
        existing_reservations,
        reservation.reservation_time
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='На текущее время, стол зарезервирован.'
        )
    return await create_reservation(reservation, session)


@router_reservations.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_reservation_router(
    id: int,
    session: AsyncSession = Depends(orm_settings.get_session)
):
    deleted_reservations_count = await delete_reservation(id, session)
    if deleted_reservations_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Номер брони ({id}) не найден.'
        )
