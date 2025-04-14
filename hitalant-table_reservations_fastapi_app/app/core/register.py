from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from routers.tables import router_tables
from routers.reservations import router_reservations

from core.exceptions import integrity_error_handler


def register_routers(app: FastAPI):
    """Регистрация эндпоинтов в приложении."""

    app.include_router(router_tables)
    app.include_router(router_reservations)


def register_exceptions(app: FastAPI):
    """Регистрация кастомных ошибок."""

    app.add_exception_handler(IntegrityError, integrity_error_handler)
