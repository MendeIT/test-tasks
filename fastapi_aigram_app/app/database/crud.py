from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ProductSchema
from database.models import Product


async def get_product_by_article(
    session: AsyncSession,
    product: ProductSchema
):
    """Получить товар из БД по артиклу."""

    query = select(Product).where(Product.article == product.article)
    result = await session.execute(query)

    return result.scalar_one_or_none()
