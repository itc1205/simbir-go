from fastapi import FastAPI
from simbir_go_backend.adapters.sqlalchemy.orm import start_mappers
from simbir_go_backend.entrypoint.controllers import (
    admin_controller,
    account_controller,
    payment_controller,
    rent_controller,
    transport_controller,
)

from simbir_go_backend.create_admin_util import create_starter_admin

start_mappers()
create_starter_admin()
app = FastAPI()

app.include_router(router=admin_controller.router, prefix="/api")
app.include_router(router=account_controller.router, prefix="/api")
app.include_router(router=transport_controller.router, prefix="/api")
app.include_router(router=rent_controller.router, prefix="/api")
app.include_router(router=payment_controller.router, prefix="/api")


@app.get("/")
def index():
    return "Hewwo, world"
