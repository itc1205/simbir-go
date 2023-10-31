from typing import Annotated
from pydantic import BaseModel

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from simbir_go_backend.config import get_auth_endpoint_url

from simbir_go_backend.service.account_services import (
    get_account_by_username,
    verify_account_password,
)
from simbir_go_backend.service.exceptions import AccountNotFound
from simbir_go_backend.service.unit_of_work import AbstractUnitOfWork

from simbir_go_backend.adapters.jwt import (
    create_access_token,
    check_if_token_banned,
    decode_token,
    ban_token,
)

from simbir_go_backend.entrypoint.dependencies.uow import get_uow

from simbir_go_backend.domain.model import Account

from simbir_go_backend.entrypoint.exceptions import (
    InvalidCredentials,
    InvalidToken,
    NotEnoughPrivileges,
)


oauth2_scheme = OAuth2PasswordBearer(get_auth_endpoint_url())


class Token(BaseModel):
    access_token: str
    token_type: str


def get_account_from_db(username: str, uow: AbstractUnitOfWork):
    try:
        return get_account_by_username(username, uow)
    except AccountNotFound:
        raise InvalidCredentials


def sign_in(form_data=Depends(OAuth2PasswordRequestForm), uow=Depends(get_uow)):
    if not verify_account_password(form_data.username, form_data.password, uow):
        raise InvalidCredentials
    return Token(
        access_token=create_access_token(data={"sub": form_data.username}),
        token_type="bearer",
    )


def sign_out(token=Depends(oauth2_scheme)):
    ban_token(token)


def get_current_account(token=Depends(oauth2_scheme), uow=Depends(get_uow)):
    if check_if_token_banned(token):
        raise InvalidToken(detail="Token is banned. Try to login again")
    username = decode_token(token)
    if username is None:
        raise InvalidToken
    account = get_account_from_db(username, uow)
    return account


def get_admin(account: Annotated[Account, Depends(get_current_account)]):
    if not account.isAdmin:
        raise NotEnoughPrivileges
    return account


