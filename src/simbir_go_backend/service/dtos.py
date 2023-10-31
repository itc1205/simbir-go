from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from simbir_go_backend.domain.model import TransportType, PriceType
from simbir_go_backend.adapters.repository import SearchTransportType


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class CreateUser(BaseModel):
    username: str
    password: str
    isAdmin: bool
    balance: float


class UpdateUser(CreateUser):
    pass


class SignUpUser(CreateUser):
    pass


class SignInUser(CreateUser):
    pass



class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    isAdmin: bool
    balance: int


class CreateTransport(BaseModel):
    ownerId: int
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    minutePrice: Optional[float] = None 
    dayPrice: Optional[float] = None

class GetClosestTransport(BaseModel):
    latitude: float
    longitude: float
    radius: float
    transportType: SearchTransportType


class UpdateTransport(CreateTransport):
    pass


class TransportInfo(CreateTransport):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CreateRent(BaseModel):
    userId: int
    transportId: int
    timeStart: datetime
    timeEnd: Optional[datetime] = None
    priceOfUnit: float
    priceType: str
    finalPrice: Optional[float] = None

class UpdateRent(CreateRent):
    pass

class EndRent(BaseModel):
    latitude: float
    longitude: float


class RentInfo(CreateRent):
    model_config = ConfigDict(from_attributes=True)
