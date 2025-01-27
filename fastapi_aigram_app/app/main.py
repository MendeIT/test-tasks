from contextlib import asynccontextmanager

import asyncio
from fastapi import FastAPI

from api.routers import router
from bot import dp, start_bot
from database.db import (
    init_models,
    shutdown
)
from core.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_models()
    scheduler.start()
    bot_task = asyncio.create_task(start_bot(dp))

    try:
        yield
    finally:
        bot_task.cancel()
        await shutdown()
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def start_app():
    return {"Hello": "World"}
