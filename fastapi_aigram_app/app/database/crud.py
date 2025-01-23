from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product


async def update_or_create_product(session: AsyncSession, product: dict):
    """Сохранение или обновление товара в БД."""

    query = select(Product).where(Product.article == product["article"])
    existing_product = await session.execute(query)
    existing_product = existing_product.scalar_one_or_none()

    if existing_product:
        existing_product.name = product["name"]
        existing_product.price = product["price"]
        existing_product.price_sale = product["price_sale"]
        existing_product.rating = product["rating"]
        existing_product.total_quantity = product["total_quantity"]
    else:
        new_product = Product(**product)
        session.add(new_product)

    await session.commit()
