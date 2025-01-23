import os

import requests
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()


async def request_data_from_wb_by_article(article: int) -> dict:
    """Получить данные с API WB по артикулу товара."""

    url = os.getenv("WB_URL") + str(article)
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Вводимый артикул не найден!"
        )

    data = response.json()
    product = await get_product_from_data(data)

    return product


async def get_product_from_data(data: dict) -> dict:
    """Получить информацию о товаре из данных."""

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
