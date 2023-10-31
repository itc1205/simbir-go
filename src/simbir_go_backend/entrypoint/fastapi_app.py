from typing import Annotated
from fastapi import FastAPI, Depends
from simbir_go_backend.adapters.sqlalchemy.orm import start_mappers
from simbir_go_backend.entrypoint.controllers import (
    admin_controller,
    account_controller,
    payment_controller,
    rent_controller,
    transport_controller,
)

start_mappers()
app = FastAPI()

app.include_router(router=admin_controller.router, prefix="/api")
app.include_router(router=account_controller.router, prefix="/api")
app.include_router(router=transport_controller.router, prefix="/api")
app.include_router(router=rent_controller.router, prefix="/api")
app.include_router(router=payment_controller.router, prefix="/api")


@app.get("/")
def index():
    return "Hewwo, world"
