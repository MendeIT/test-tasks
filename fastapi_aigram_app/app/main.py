from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ProductBaseSchema
from core.requests import request_data_from_wb_by_article
from database.db import get_session, init_models, shutdown, drop_models
from database.crud import update_or_create_product


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()

    yield

    await shutdown()
    await drop_models()


app = FastAPI(root_path="/api/v1", lifespan=lifespan)


@app.get("/")
async def start_app():
    return {"Hello": "World"}


@app.post("/products/")
async def get_products(
    product: ProductBaseSchema,
    session: AsyncSession = Depends(get_session)
):
    new_product = await request_data_from_wb_by_article(product.article)
    await update_or_create_product(session=session, product=new_product)

    return new_product
