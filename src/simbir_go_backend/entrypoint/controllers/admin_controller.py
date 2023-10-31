from fastapi import APIRouter, Depends

from simbir_go_backend.entrypoint.dependencies.uow import get_uow
from simbir_go_backend.entrypoint.dependencies.auth import get_admin
from simbir_go_backend.service import (
    account_services,
    rent_services,
    transport_services,
)
from simbir_go_backend.service.exceptions import (
    AccountNotFound,
    AccountAlreadyExists,
    TransportNotFound,
    RentNotFound,
)
from simbir_go_backend.entrypoint.exceptions import EntityNotFound, LoginAlreadyExists

from simbir_go_backend.service.dtos import (
    CreateTransport,
    CreateUser,
    CreateRent,
    UpdateRent,
    EndRent,
)

router = APIRouter(
    prefix="/Admin", tags=["AdminController"], dependencies=[Depends(get_admin)]
)


@router.get("/ping")
def ping_admin():
    return "pong!"


@router.post("/User")
def create_account(data: CreateUser, uow=Depends(get_uow)):
    try:
        account_services.create_new_user(data, uow)
    except AccountAlreadyExists:
        raise LoginAlreadyExists
    return 200


@router.get("/User")
def get_accounts(start: int, count: int, uow=Depends(get_uow)):
    return account_services.read_all_accounts(start, count, uow)


@router.get("/User/{id:int}")
def get_account(id: int, uow=Depends(get_uow)):
    return account_services.read_account_by_id(id, uow)


@router.delete("/User/{id:int}")
def delete_account(id: int, uow=Depends(get_uow)):
    try:
        account_services.delete_user(id, uow)
    except AccountNotFound:
        raise EntityNotFound(detail="Account not found")
    return 200


@router.post("/Transport")
def create_transport(data: CreateTransport, uow=Depends(get_uow)):
    try:
        transport_services.create_new_transport(data, uow)
    except AccountNotFound:
        raise EntityNotFound(detail="Account of owner not found")
    return 200


@router.get("/Transport")
def list_transport(start: int, count: int, uow=Depends(get_uow)):
    return transport_services.read_all_transport(start, count, uow)


@router.delete("/Transport/{id:int}")
def delete_transport(id: int, uow=Depends(get_uow)):
    try:
        transport_services.delete_transport(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport not found")
    return 200


@router.get("/Transport{id:int}")
def get_transport(id: int, uow=Depends(get_uow)):
    try:
        transport_services.read_transport_by_id(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport not found")
    return 200


@router.get("/Rent/{id:int}")
def get_info_about_rent(id: int, uow=Depends(get_uow)):
    try:
        rent_services.read_rent_by_id(id, uow)
    except RentNotFound:
        raise EntityNotFound(detail="Rent not found")


@router.get("/Rent/UserHistory/{id:int}")
def get_user_rent_history(id: int, uow=Depends(get_uow)):
    try:
        return rent_services.get_account_history(id, uow)
    except AccountNotFound:
        raise EntityNotFound(detail="Account not found")


@router.get("/Rent/TransportHistory/{id:int}")
def get_transport_rent_history(id: int, uow=Depends(get_uow)):
    try:
        return rent_services.get_transport_history(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport not found")


@router.post("/Rent")
def create_new_rent(data: CreateRent, uow=Depends(get_uow)):
    try:
        rent_services.create_new_rent(data, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport not found")
    except AccountNotFound:
        raise EntityNotFound(detail="Account not found")
    return 200


@router.put("/Rent/{id:int}")
def update_rent(id: int, data: UpdateRent, uow=Depends(get_uow)):
    try:
        rent_services.update_rent(id, data, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport not found")
    except AccountNotFound:
        raise EntityNotFound(detail="Account not found")
    return 200


@router.post("/Rent/End/{id:int}")
def end_rent(id: int, data: EndRent, uow=Depends(get_uow)):
    try:
        rent_services.end_rent(id, data, uow)
    except RentNotFound:
        raise EntityNotFound(detail="Rent not found")
    return 200

@router.delete("/Rent/{id:int}")
def delete_rent(id: int, uow=Depends(get_uow)):
    try:
        rent_services.delete_rent(id, uow)
    except RentNotFound:
        raise EntityNotFound(detail="Rent not found")
    return 200