import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.db.database import orm_settings
from app.core.register import register_exceptions, register_routers
from app.core.exceptions import integrity_error_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_routers(app)
    register_exceptions(app)

    if settings.DEBUG:
        await orm_settings._init_models()

    yield

    await orm_settings.shutdown_session()


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        lifespan=lifespan,
        exception_handlers={
            IntegrityError: integrity_error_handler,
        }
    )
    return app


app = create_app()


def start_server(app: FastAPI):
    """Запуск Uvicorn-сервера."""

    uvicorn.run(
        app,
        host=settings.UVICORN_HOST,
        port=int(settings.UVICORN_PORT),
        reload=False
    )


if __name__ == "__main__":
    try:
        start_server(app)
    except KeyboardInterrupt:
        message = 'Interrupted!'
        print(f'{message:_^50}')
        sys.exit(0)
    except Exception as error:
        print('Что-то пошло не так, приложение остановлено!')
        raise error
