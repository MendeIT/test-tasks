import pytest
from httpx import AsyncClient, codes
from app.main import app


@pytest.mark.anyio
async def test_create_reservation():
    """Тест. Создание резерва стола."""

    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post(
            '/reservations/',
            json={
                'customer_name': 'Test User',
                'reservation_time': '2025-04-15T14:00:00+03:00',
                'duration_minutes': 60,
                'table_id': 1
            }
        )
    assert response.status_code in (codes.OK, codes.CREATED)
