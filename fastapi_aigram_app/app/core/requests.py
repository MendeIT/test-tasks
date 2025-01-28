from typing import Any

import requests
from fastapi import HTTPException

from api.schemas import ProductSchema
from core.conf import settings
from database.crud import get_product_by_article
from database.db import get_session
from database.models import Product


async def request_data_from_wb_by_article(article: int):
    """Получить данные с API WB по артикулу товара."""

    url = settings.WB_URL + str(article)

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Вводимый артикул не найден!"
        )

    return response.json()


async def clear_product_data(data: Any) -> dict:
    """Очитка данных о товаре из данных."""

    try:
        product = data['data']['products'][0]
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Неизвестный формат данных от WB! {error}"
        )
    else:
        return {
            "name": product.get('name'),
            "article": product.get('id'),
            "price": product.get('priceU') / 100,
            "price_sale": product.get('salePriceU') / 100,
            "rating": product.get('rating', None),
            "total_quantity": product.get('totalQuantity'),
        }


async def periodic_get_data(article):
    """Метод переодического обнавления данных."""

    data = await request_data_from_wb_by_article(article)
    clear_data = await clear_product_data(data)
    product = ProductSchema(**clear_data)

    async with get_session() as session:
        existing_product = await get_product_by_article(session, product)
        if existing_product is None:
            new_product = Product(
                article=product.article,
                name=product.name,
                price=product.price,
                price_sale=product.price_sale,
                rating=product.rating,
                total_quantity=product.total_quantity,
            )
            session.add(new_product)
            await session.commit()
            await session.refresh(new_product)
