from simbir_go_backend.domain.model import Account
from simbir_go_backend.service.unit_of_work import AbstractUnitOfWork
from simbir_go_backend.service.exceptions import AccountAlreadyExists, AccountNotFound


def create_new_user(
    username: str, password: str, isAdmin: bool, balance: float, uow: AbstractUnitOfWork
):
    with uow:
        if uow.accounts.get_by_username(username) is not None:
            raise AccountAlreadyExists
        account = Account(username, password, isAdmin, balance, disabledToken=False)
        uow.accounts.add(account)
        uow.commit()


def update_user(
    id: int,
    username: str,
    password: str,
    isAdmin: bool,
    balance: float,
    uow: AbstractUnitOfWork,
):
    with uow:
        account = uow.accounts.get(id)
        if account is None:
            raise AccountNotFound
        account.username = username
        account.password = password
        account.isAdmin = isAdmin
        account.balance = balance
        uow.commit()


def read_user_by_id(id: int, uow: AbstractUnitOfWork):
    with uow:
        account = uow.accounts.get(id)
        if account is None:
            raise AccountNotFound
        return account


def delete_user(id: int, uow: AbstractUnitOfWork):
    with uow:
        account = uow.accounts.get(id)
        if account is None:
            raise AccountNotFound
        uow.accounts.delete(account)
        uow.commit()
