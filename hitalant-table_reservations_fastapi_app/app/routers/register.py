from fastapi import FastAPI
from .tables import router_tables
from .reservations import router_reservations


def register_routers(app: FastAPI):
    app.include_router(router_tables)
    app.include_router(router_reservations)
