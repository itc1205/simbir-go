from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class TransportType(str, Enum):
    Car = "Car"
    Bike = "Bike"
    Scooter = "Scooter"


class PriceType(str, Enum):
    Minutes = "Minutes"
    Days = "Days"


@dataclass
class Account:
    username: str
    password: str
    isAdmin: bool
    balance: float


@dataclass
class Transport:
    owner: Account
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]


@dataclass
class Rent:
    transport: Transport
    user: Account
    timeStart: datetime
    timeEnd: Optional[datetime]
    priceOfUnit: float
    priceType: PriceType
    finalPrice: Optional[float]


def HESOYAM(account: Account):
    account.balance += 250_000


def rent_transport(
    transport: Transport,
    user: Account,
    timeStart: datetime,
    timeEnd: Optional[datetime],
    priceOfUnit: float,
    priceType: PriceType,
    finalPrice: Optional[float],
) -> Rent:
    return Rent(transport, user, timeStart, timeEnd, priceOfUnit, priceType, finalPrice)
