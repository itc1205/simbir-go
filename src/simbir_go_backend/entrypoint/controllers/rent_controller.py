from datetime import datetime
from fastapi import APIRouter, Depends

from simbir_go_backend.service import (
    rent_services,
    transport_services,
)
from simbir_go_backend.entrypoint.dependencies.auth import get_current_account
from simbir_go_backend.entrypoint.dependencies.uow import get_uow

from simbir_go_backend.entrypoint import schemas
from simbir_go_backend.service import dtos

from simbir_go_backend.service.exceptions import (
    RentNotFound,
    TransportNotFound,
    UnrentableTransport,
)
from simbir_go_backend.entrypoint.exceptions import EntityNotFound, NotEnoughPrivileges

router = APIRouter(prefix="/Rent", tags=["RentController"])


@router.post("/Transport")
def get_closest_transport(data: schemas.GetClosestTransport, uow=Depends(get_uow)):
    return transport_services.get_closest_transport(
        dtos.GetClosestTransport.model_validate(data.model_dump()), uow
    )


@router.get("/{id:int}")
def get_info_rent(id: int, uow=Depends(get_uow), user=Depends(get_current_account)):
    try:
        rent = rent_services.read_rent_by_id(id, uow)
    except RentNotFound:
        raise EntityNotFound(detail="Rent does not exist")
    try:
        transport = transport_services.read_transport_by_id(rent.transportId, uow)
    except TransportNotFound:
        raise EntityNotFound(
            detail="Horrible thing happened, please ask the administrator"
        )
    if user.id != transport.ownerId and user.id != rent.userId:
        raise NotEnoughPrivileges
    return 200


@router.get("/MyHistory")
def get_info_about_rents(uow=Depends(get_uow), user=Depends(get_current_account)):
    return rent_services.get_account_history(user.id, uow)


@router.get("/TransportHistory/{id:int}")
def get_info_about_transport(
    id: int, uow=Depends(get_uow), user=Depends(get_current_account)
):
    try:
        transport = transport_services.read_transport_by_id(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport does not exist")
    if transport.ownerId != user.id:
        raise NotEnoughPrivileges
    return rent_services.get_transport_history(id, uow)


@router.post("/New/{id:int}")
def create_new_rent(
    id: int,
    data: schemas.CreateRent,
    uow=Depends(get_uow),
    user=Depends(get_current_account),
):
    try:
        transport = transport_services.read_transport_by_id(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport does not exist")

    if transport.ownerId == user.id:
        raise NotEnoughPrivileges(detail="You cant rent your own transport, dummy!")

    try:
        priceOfUnit = transport_services.calculatePriceOfUnit(transport)
    except UnrentableTransport:
        raise EntityNotFound(detail="Transport is not available for rents")
    rent_services.create_new_rent(
        dtos.CreateRent(
            priceOfUnit=priceOfUnit,
            userId=user.id,
            transportId=transport.id,
            timeStart=datetime.now(),
            priceType=data.priceType,
        ),
        uow,
    )
    return 200


@router.post("/End/{id:int}")
def end_rent(
    id: int,
    data: schemas.EndRent,
    uow=Depends(get_uow),
    user=Depends(get_current_account),
):
    try:
        rent_services.end_rent(id, dtos.EndRent.model_validate(data.model_dump()), uow)
    except RentNotFound:
        raise EntityNotFound(detail="Rent not found")
    return 200
