from typing import Optional
from datetime import datetime
from simbir_go_backend.domain.model import Rent, PriceType, rent_transport, calculate_final_price
from simbir_go_backend.service.unit_of_work import AbstractUnitOfWork
from simbir_go_backend.service.exceptions import (
    AccountNotFound,
    TransportNotFound,
    RentNotFound,
)

from simbir_go_backend.service.dtos import CreateRent, UpdateRent, EndRent, RentInfo


def create_new_rent(
    data: CreateRent,
    uow: AbstractUnitOfWork,
):
    with uow:
        account = uow.accounts.get(data.userId)
        if account is None:
            raise AccountNotFound
        transport = uow.transport.get(data.transportId)
        if transport is None:
            raise TransportNotFound
        rent = rent_transport(
            transport,
            account,
            data.timeStart,
            data.timeEnd,
            data.priceOfUnit,
            PriceType(data.priceType),
            data.finalPrice,
        )
        uow.rents.add(rent)
        uow.commit()


def read_rent_by_id(id: int, uow: AbstractUnitOfWork):
    with uow:
        rent = uow.rents.get(id)
        if rent is None:
            raise RentNotFound
        return RentInfo.model_validate(rent)


def update_rent(
    id: int,
    data: UpdateRent,
    uow: AbstractUnitOfWork,
):
    with uow:
        rent = uow.rents.get(id)
        if rent is None:
            raise RentNotFound
        account = uow.accounts.get(data.userId)
        if account is None:
            raise AccountNotFound
        transport = uow.transport.get(data.transportId)
        if transport is None:
            raise TransportNotFound
        rent.user = account
        rent.transport = transport
        rent.timeStart = data.timeStart
        rent.timeEnd = data.timeEnd
        rent.priceOfUnit = data.priceOfUnit
        rent.priceType = PriceType(data.priceType)
        rent.finalPrice = data.finalPrice
        uow.commit()


def delete_rent(id: int, uow: AbstractUnitOfWork):
    with uow:
        rent = uow.rents.get(id)
        if rent is None:
            raise RentNotFound
        uow.rents.delete(rent)
        uow.commit()


def get_account_history(id: int, uow: AbstractUnitOfWork):
    with uow:
        if not uow.accounts.get(id):
            raise AccountNotFound
        rents = uow.rents.get_from_user(id)
        return [RentInfo.model_validate(ent) for ent in rents]


def get_transport_history(id: int, uow: AbstractUnitOfWork):
    with uow:
        if not uow.transport.get(id):
            raise TransportNotFound
        rents = uow.rents.get_from_transport(id)
        return [RentInfo.model_validate(ent) for ent in rents]


def end_rent(id:int, data: EndRent, uow: AbstractUnitOfWork):
    with uow:
        rent = uow.rents.get(id)
        if not rent:
            raise RentNotFound
        
        rent.transport.canBeRented = True
        rent.transport.latitude = data.latitude
        rent.transport.longitude = data.longitude
        rent.timeEnd = datetime.now()
        
        rent.finalPrice = calculate_final_price(rent)
        
        uow.commit()
        