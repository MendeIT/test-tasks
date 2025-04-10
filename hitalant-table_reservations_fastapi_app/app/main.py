import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from routers.register import register_routers
from core.config import settings
# from db.database import orm_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_routers(app)
    # if settings.DEBUG:
    #     await orm_settings.init_models()

    yield
    # await orm_settings.shutdown()


app = FastAPI(debug=settings.DEBUG, lifespan=lifespan)


def start_server():
    """Запуск Uvicorn-сервера."""

    uvicorn.run(
        app,
        host=settings.UVICORN_HOST,
        port=int(settings.UVICORN_PORT),
        reload=False
    )


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        message = 'Interrupted!'
        print(f'{message:_^50}')
        sys.exit(0)
    except Exception as error:
        print('Что-то пошло не так, приложение остановлено!')
        raise error
