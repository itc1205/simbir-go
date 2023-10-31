from simbir_go_backend.service.account_services import create_new_user
from simbir_go_backend.service.dtos import CreateUser
from simbir_go_backend.entrypoint.dependencies.uow import get_uow
from simbir_go_backend.adapters.sqlalchemy.orm import start_mappers
from simbir_go_backend.config import get_admin_credentials
from simbir_go_backend.service.exceptions import AccountAlreadyExists


def create_starter_admin():
    (username, password, balance) = get_admin_credentials()
    user = CreateUser(
        username=username, password=password, isAdmin=True, balance=balance
    )
    uow = next(get_uow())
    try:
        create_new_user(user, uow)
    except AccountAlreadyExists:
        pass
