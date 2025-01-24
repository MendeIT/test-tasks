from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import router
from database.db import (
    init_models,
    drop_models,
    shutdown
)
from core.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    scheduler.start()

    yield

    scheduler.shutdown()
    await drop_models()
    await shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def start_app():
    return {"Hello": "World"}
