from simbir_go_backend.domain.model import Account
from simbir_go_backend.service.unit_of_work import AbstractUnitOfWork
from simbir_go_backend.service.exceptions import AccountAlreadyExists, AccountNotFound
from simbir_go_backend.service.dtos import CreateUser, UserInfo, UpdateUser
from simbir_go_backend.adapters.security import verify_password, hash_password


def create_new_user(data: CreateUser, uow: AbstractUnitOfWork):
    with uow:
        if uow.accounts.get_by_username(data.username) is not None:
            raise AccountAlreadyExists
        account = Account(
            data.username,
            hash_password(data.password),
            data.isAdmin,
            data.balance,
        )
        uow.accounts.add(account)
        uow.commit()


def update_user(
    id: int,
    data: UpdateUser,
    uow: AbstractUnitOfWork,
):
    with uow:
        account = uow.accounts.get(id)
        if account is None:
            raise AccountNotFound
        account.username = data.username
        account.password = hash_password(data.password)
        account.isAdmin = data.isAdmin
        account.balance = data.balance
        uow.commit()


def get_account_by_username(username: str, uow: AbstractUnitOfWork):
    with uow:
        account = uow.accounts.get_by_username(username)
        if account is None:
            raise AccountNotFound
        return UserInfo.model_validate(account)


def read_all_accounts(begin: int, end: int, uow: AbstractUnitOfWork):
    with uow:
        accounts = uow.accounts.list(begin, end)
        return [UserInfo.model_validate(ent) for ent in accounts]


def read_account_by_id(id: int, uow: AbstractUnitOfWork):
    with uow:
        account = uow.accounts.get(id)
        if account is None:
            raise AccountNotFound
        return UserInfo.model_validate(account)


def delete_user(id: int, uow: AbstractUnitOfWork):
    with uow:
        account = uow.accounts.get(id)
        if account is None:
            raise AccountNotFound
        uow.accounts.delete(account)
        uow.commit()


def verify_account_password(username: str, password: str, uow: AbstractUnitOfWork):
    with uow:
        account = uow.accounts.get_by_username(username)
        if account is None:
            return False
        return verify_password(password, account.password)


def HESOYAM(id: int, uow: AbstractUnitOfWork):
    with uow:
        account = uow.accounts.get(id)
        if account is None:
            raise AccountNotFound
        account.balance += 250_000
        uow.commit()
