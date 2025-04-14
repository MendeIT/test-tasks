import pytest
from httpx import AsyncClient
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Table, Reservation


@pytest.mark.asyncio
async def test_example(client: AsyncClient) -> None:

    response = await client.get('/api/v1/test/')

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_routes_registered(client: AsyncClient):

    response = await client.get("/openapi.json")
    paths = response.json()["paths"]

    assert "/api/v1/test/" in paths
    assert "/api/v1/tables/" in paths
    assert "/api/v1/reservations/" in paths


@pytest.mark.asyncio
async def test_create_reservation(
    client: AsyncClient,
    session: AsyncSession
) -> None:
    """Тест cоздания резерва стола."""

    await session.execute(delete(Reservation))
    await session.execute(delete(Table))

    valid_table = {
        "table_id": 1,
        "name": "Стол 1",
        "seats": 4,
        "location": "Терраса"
    }

    await session.execute(insert(Table).values(valid_table))
    await session.commit()

    response = await client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Иван Иванов",
            "reservation_time": "2025-04-15T14:00:00+03:00",
            "duration_minutes": 60,
            "table_id": 1
        }
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_conflicts_reservation(
    client: AsyncClient,
    session: AsyncSession,
    test_tables
) -> None:
    """Тест конфликта бронирований."""

    response = await client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Иван Иванов",
            "reservation_time": "2025-04-15T14:00:00+03:00",
            "duration_minutes": 60,
            "table_id": 1
        }
    )
    assert response.status_code == 201

    failed_response = await client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Петр Петров",
            "reservation_time": "2025-04-15T14:10:00+03:00",
            "duration_minutes": 60,
            "table_id": 1
        }
    )
    assert failed_response.status_code == 400
