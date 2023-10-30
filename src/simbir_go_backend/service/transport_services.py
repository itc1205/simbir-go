from typing import Optional
from simbir_go_backend.domain.model import Transport, TransportType
from simbir_go_backend.service.unit_of_work import AbstractUnitOfWork
from simbir_go_backend.service.exceptions import AccountNotFound, TransportNotFound


def create_new_transport(
    ownerId: int,
    canBeRented: bool,
    transportType: str,
    model: str,
    color: str,
    identifier: str,
    description: Optional[str],
    latitude: float,
    longitude: float,
    minutePrice: Optional[float],
    dayPrice: Optional[float],
    uow: AbstractUnitOfWork,
):
    with uow:
        owner = uow.accounts.get(ownerId)
        if owner is None:
            raise AccountNotFound
        transport = Transport(
            owner,
            canBeRented,
            TransportType(transportType),
            model,
            color,
            identifier,
            description,
            latitude,
            longitude,
            minutePrice,
            dayPrice,
        )
        uow.transport.add(transport)
        uow.commit()


def update_transport(
    id: int,
    ownerId: int,
    canBeRented: bool,
    transportType: str,
    model: str,
    color: str,
    identifier: str,
    description: Optional[str],
    latitude: float,
    longitude: float,
    minutePrice: Optional[float],
    dayPrice: Optional[float],
    uow: AbstractUnitOfWork,
):
    with uow:
        transport = uow.transport.get(id)
        if transport is None:
            raise TransportNotFound

        owner = uow.accounts.get(ownerId)
        if owner is None:
            raise AccountNotFound

        transport.owner = owner
        transport.canBeRented = canBeRented
        transport.transportType = TransportType(transportType)
        transport.model = model
        transport.color = color
        transport.identifier = identifier
        transport.description = description
        transport.latitude = latitude
        transport.longitude = longitude
        transport.minutePrice = minutePrice
        transport.dayPrice = dayPrice

        uow.commit()


def read_transport_by_id(id: int, uow: AbstractUnitOfWork):
    with uow:
        transport = uow.transport.get(id)
        if transport is None:
            raise TransportNotFound
        return transport


def delete_transport(id: int, uow: AbstractUnitOfWork):
    with uow:
        transport = uow.transport.get(id)
        if transport is None:
            raise TransportNotFound
        uow.transport.delete(transport)
        uow.commit()
