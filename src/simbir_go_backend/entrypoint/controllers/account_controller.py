from fastapi import APIRouter, Depends

from simbir_go_backend.entrypoint.dependencies.uow import get_uow
from simbir_go_backend.entrypoint.dependencies.auth import (
    get_current_account,
    sign_in,
    sign_out,
)
from simbir_go_backend.service import account_services
from simbir_go_backend.service.exceptions import (
    AccountNotFound,
    AccountAlreadyExists,
)
from simbir_go_backend.entrypoint.exceptions import EntityNotFound, LoginAlreadyExists

from simbir_go_backend.service import dtos
from simbir_go_backend.entrypoint import schemas

router = APIRouter(prefix="/Account", tags=["AccountController"])


@router.post("/SignUp")
def create_account(data: schemas.CreateUser, uow=Depends(get_uow)):
    try:
        return account_services.create_new_user(
            dtos.CreateUser(
                username=data.username, password=data.password, isAdmin=False, balance=0
            ),
            uow,
        )
    except AccountAlreadyExists:
        raise LoginAlreadyExists


@router.post("/SignIn")
def login(token=Depends(sign_in)):
    return token


@router.post("/SignOut")
def logout(_=Depends(sign_out)):
    return 200


@router.put("/Update")
def update_account(
    data: schemas.UpdateUser, uow=Depends(get_uow), user=Depends(get_current_account)
):
    try:
        account_services.update_user(
            user.id,
            dtos.UpdateUser(
                username=data.username,
                password=data.password,
                isAdmin=user.isAdmin,
                balance=user.balance,
            ),
            uow,
        )
    except AccountNotFound:
        raise EntityNotFound


@router.get("/Me")
def me(user=Depends(get_current_account)):
    return user
