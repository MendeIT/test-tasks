from contextlib import asynccontextmanager

import asyncio
from fastapi import FastAPI

from api.routers import router
from bot import BOT, dp
from database.db import (
    init_models,
    shutdown
)
from core.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_models()
    scheduler.start()
    bot_task = asyncio.create_task(dp.start_polling(BOT))

    try:
        yield
    finally:
        dp.stop_polling()
        bot_task.cancel()
        await shutdown()
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(router=router)
