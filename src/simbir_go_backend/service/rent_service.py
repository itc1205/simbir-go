from typing import Optional
from datetime import datetime
from simbir_go_backend.domain.model import Rent, PriceType
from simbir_go_backend.service.unit_of_work import AbstractUnitOfWork
from simbir_go_backend.service.exceptions import (
    AccountNotFound,
    TransportNotFound,
    RentNotFound,
)


def create_new_rent(
    account_id: int,
    transport_id: int,
    timeStart: datetime,
    timeEnd: Optional[datetime],
    priceOfUnit: float,
    priceType: str,
    finalPrice: Optional[float],
    uow: AbstractUnitOfWork,
):
    with uow:
        account = uow.accounts.get(account_id)
        if account is None:
            raise AccountNotFound
        transport = uow.transport.get(transport_id)
        if transport is None:
            raise TransportNotFound
        rent = Rent(
            transport,
            account,
            timeStart,
            timeEnd,
            priceOfUnit,
            PriceType(priceType),
            finalPrice,
        )
        uow.rents.add(rent)
        uow.commit()


def read_rent_by_id(id: int, uow: AbstractUnitOfWork):
    with uow:
        rent = uow.rents.get(id)
        if rent is None:
            raise RentNotFound
        return rent


def update_rent(
    id: int,
    account_id: int,
    transport_id: int,
    timeStart: datetime,
    timeEnd: Optional[datetime],
    priceOfUnit: float,
    priceType: str,
    finalPrice: Optional[float],
    uow: AbstractUnitOfWork,
):
    with uow:
        rent = uow.rents.get(id)
        if rent is None:
            raise RentNotFound
        account = uow.accounts.get(account_id)
        if account is None:
            raise AccountNotFound
        transport = uow.transport.get(transport_id)
        if transport is None:
            raise TransportNotFound
        rent.user = account
        rent.transport = transport
        rent.timeStart = timeStart
        rent.timeEnd = timeEnd
        rent.priceOfUnit = priceOfUnit
        rent.priceType = PriceType(priceType)
        rent.finalPrice = finalPrice
        uow.commit()


def delete_rent(id: int, uow: AbstractUnitOfWork):
    with uow:
        rent = uow.rents.get(id)
        if rent is None:
            raise RentNotFound
        uow.rents.delete(rent)
        uow.commit()
