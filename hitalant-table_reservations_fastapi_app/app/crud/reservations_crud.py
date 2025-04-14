from datetime import datetime, timezone, timedelta

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Reservation
from schemas.reservations_schema import ReservationCreateSchema


async def create_reservation(
    data: ReservationCreateSchema,
    session: AsyncSession
) -> Reservation:
    """Создание резерва стола."""

    reservation = Reservation(**data.model_dump(exclude_none=True))
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)

    return reservation


async def get_list_reservations(session: AsyncSession) -> list[Reservation]:
    """Получить список зарезервированных столов."""

    query = select(Reservation)
    result = await session.execute(query)

    return result.scalars().all()


async def delete_reservation(
    reservation_id: int,
    session: AsyncSession
) -> int:
    """Удалить резерв стола. Возвращает кол-во удалённых записей."""

    query = delete(Reservation).where(
        Reservation.reservation_id == reservation_id
    )
    result = await session.execute(query)
    await session.commit()

    return result.rowcount


async def get_reservations_by_table(
    reservation: ReservationCreateSchema,
    session: AsyncSession
) -> list[Reservation]:
    """Получить резервы на указанный стол."""

    query = select(Reservation).where(
        (Reservation.table_id == reservation.table_id) &
        (Reservation.reservation_time <= reservation.reservation_time)
    )
    result = await session.execute(query)

    return result.scalars().all()


def check_reserved(
    reservations: list[Reservation],
    new_start_time_reserved: datetime
) -> bool:
    """Проверка на пересечение брони."""

    for reserved in reservations:
        exist_time_end = reserved.reservation_time + timedelta(
            minutes=reserved.duration_minutes
        )
        if exist_time_end.replace(
            tzinfo=timezone.utc
        ) > new_start_time_reserved:

            return False

    return True
