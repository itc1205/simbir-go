from typing import Optional
from simbir_go_backend.domain.model import Transport, TransportType
from simbir_go_backend.service.dtos import (
    CreateTransport,
    TransportInfo,
    UpdateTransport,
    GetClosestTransport
)
from simbir_go_backend.service.unit_of_work import AbstractUnitOfWork
from simbir_go_backend.service.exceptions import AccountNotFound, TransportNotFound, UnrentableTransport


def create_new_transport(
    data: CreateTransport,
    uow: AbstractUnitOfWork,
):
    with uow:
        owner = uow.accounts.get(data.ownerId)
        if owner is None:
            raise AccountNotFound
        transport = Transport(
            owner,
            data.canBeRented,
            TransportType(data.transportType),
            data.model,
            data.color,
            data.identifier,
            data.description,
            data.latitude,
            data.longitude,
            data.minutePrice,
            data.dayPrice,
        )
        uow.transport.add(transport)
        uow.commit()


def update_transport(
    id: int,
    data: UpdateTransport,
    uow: AbstractUnitOfWork,
):
    with uow:
        transport = uow.transport.get(id)
        if transport is None:
            raise TransportNotFound

        owner = uow.accounts.get(data.ownerId)
        if owner is None:
            raise AccountNotFound

        transport.owner = owner
        transport.canBeRented = data.canBeRented
        transport.transportType = TransportType(data.transportType)
        transport.model = data.model
        transport.color = data.color
        transport.identifier = data.identifier
        transport.description = data.description
        transport.latitude = data.latitude
        transport.longitude = data.longitude
        transport.minutePrice = data.minutePrice
        transport.dayPrice = data.dayPrice

        uow.commit()


def read_transport_by_id(id: int, uow: AbstractUnitOfWork):
    with uow:
        transport = uow.transport.get(id)
        if transport is None:
            raise TransportNotFound
        return TransportInfo.model_validate(transport)


def delete_transport(id: int, uow: AbstractUnitOfWork):
    with uow:
        transport = uow.transport.get(id)
        if transport is None:
            raise TransportNotFound
        uow.transport.delete(transport)
        uow.commit()


def read_all_transport(begin: int, end: int, uow: AbstractUnitOfWork):
    with uow:
        transport = uow.transport.list(begin, end)
        return [TransportInfo.model_validate(ent) for ent in transport]


def get_closest_transport(
    data: GetClosestTransport, uow: AbstractUnitOfWork
):
    with uow:
        transport = uow.transport.list_closest(data.longitude, data.latitude, data.radius, data.transportType)
        return [TransportInfo.model_validate(ent) for ent in transport]

def calculatePriceOfUnit(transport: TransportInfo):
    if transport.dayPrice is not None:
        return transport.dayPrice
    elif transport.minutePrice is not None:
        return transport.minutePrice
    else:
        raise UnrentableTransport