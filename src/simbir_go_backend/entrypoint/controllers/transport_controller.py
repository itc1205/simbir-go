from fastapi import APIRouter, Depends

from simbir_go_backend.service import dtos
from simbir_go_backend.entrypoint import schemas
from simbir_go_backend.service import transport_services

from simbir_go_backend.entrypoint.dependencies.uow import get_uow
from simbir_go_backend.entrypoint.dependencies.auth import get_current_account

from simbir_go_backend.service.exceptions import TransportNotFound
from simbir_go_backend.entrypoint.exceptions import EntityNotFound, NotEnoughPrivileges

router = APIRouter(prefix="/Transport", tags=["TransportController"])


@router.get("/{id:int}")
def get_transport(id: int, uow=Depends(get_uow)):
    try:
        return transport_services.read_transport_by_id(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport does not exists")
    

@router.post("/")
def create_transport(
    data: schemas.CreateTransport,
    uow=Depends(get_uow),
    user=Depends(get_current_account),
):
    transport_services.create_new_transport(
        dtos.CreateTransport(
            ownerId=user.id,
            canBeRented=data.canBeRented,
            transportType=data.transportType,
            model=data.model,
            color=data.color,
            identifier=data.identifier,
            description=data.description,
            latitude=data.latitude,
            longitude=data.longitude,
            minutePrice=data.minutePrice,
            dayPrice=data.dayPrice,
        ),
        uow,
    )
    return 200


@router.put("/{id:int}")
def update_transport(
    id: int,
    data: schemas.UpdateTransport,
    uow=Depends(get_uow),
    user=Depends(get_current_account),
):
    try:
        transport = transport_services.read_transport_by_id(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport not found")

    if transport.ownerId != user.id:
        raise NotEnoughPrivileges(detail="You do not own this transport")

    transport_services.update_transport(
        id,
        dtos.UpdateTransport(
            ownerId=user.id,
            canBeRented=data.canBeRented,
            transportType=data.transportType,
            model=data.model,
            color=data.color,
            identifier=data.identifier,
            description=data.description,
            latitude=data.latitude,
            longitude=data.longitude,
            minutePrice=data.minutePrice,
            dayPrice=data.dayPrice,
        ),
        uow,
    )
    return 200


@router.delete("/{id:int}")
def delete_transport(id: int, uow=Depends(get_uow), user=Depends(get_current_account)):
    try:
        transport = transport_services.read_transport_by_id(id, uow)
    except TransportNotFound:
        raise EntityNotFound(detail="Transport not found")

    if transport.ownerId != user.id:
        raise NotEnoughPrivileges(detail="You do not own this transport")

    transport_services.delete_transport(id, uow)
    return 200
