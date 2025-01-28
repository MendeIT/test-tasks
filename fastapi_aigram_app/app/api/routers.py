from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ProductBaseSchema, ProductSchema
from core.requests import (
    clear_product_data,
    periodic_get_data,
    request_data_from_wb_by_article,
)
from core.conf import settings
from core.scheduler import scheduler
from database.crud import get_product_by_article
from database.db import get_session
from database.models import Product


router = APIRouter(prefix="/api/v1")


@router.post("/products/")
async def get_products(
    product: ProductBaseSchema,
    session: AsyncSession = Depends(get_session)
):
    data = await request_data_from_wb_by_article(product.article)
    clear_data = await clear_product_data(data)
    new_product = ProductSchema(**clear_data)

    async with get_session() as session:
        product_db = await get_product_by_article(
            session=session,
            product=new_product
        )

        if product_db:
            product_db.name = new_product.name
            product_db.price = new_product.price
            product_db.price_sale = new_product.price_sale
            product_db.rating = new_product.rating
            product_db.total_quantity = new_product.total_quantity
        else:
            session.add(Product(**new_product.model_dump()))

        await session.commit()

    return {'success': 'Новый товар добавлен или обнавлен!'}


@router.get("/subscribe/{article}")
async def subscribe_to_product(article: int):

    job_id = f"product_{article}"

    if scheduler.get_job(job_id):
        return {"message": "Вы уже подписаны на этот товар."}

    scheduler.add_job(
        periodic_get_data,
        "interval",
        minutes=int(settings.INTERVAL),
        id=job_id,
        kwargs={"article": article}
    )
    return {"message": "Вы подписались на товар."}
