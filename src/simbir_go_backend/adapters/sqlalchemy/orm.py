from sqlalchemy import (
    Column,
    Table,
    ForeignKey,
    DateTime,
    String,
    Boolean,
    Integer,
    Float,
)
from sqlalchemy.orm import relationship, registry

from simbir_go_backend.domain.model import Account, Transport, Rent
from simbir_go_backend.adapters.sqlalchemy.custom_types import (
    OrmPriceType,
    OrmTransportType,
)

mapper_registry = registry()
metadata = mapper_registry.metadata

accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, autoincrement=True, unique=True),
    Column("username", String(255), unique=True),
    Column("isAdmin", Boolean),
    Column("balance", Float),
)

transports = Table(
    "transports",
    metadata,
    Column("id", Integer, autoincrement=True, unique=True),
    Column("ownerId", ForeignKey("accounts.id")),
    Column("canBeRented", Boolean),
    Column("transportType", OrmTransportType),
    Column("model", String(255)),
    Column("color", String(255)),
    Column("identifier", String(255)),
    Column("description", String(255), nullable=True),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("minutePrice", Float, nullable=True),
    Column("dayPrice", Float, nullable=True),
)

rents = Table(
    "rents",
    metadata,
    Column("id", Integer, autoincrement=True, unique=True),
    Column("userId", ForeignKey("accounts.id")),
    Column("transportId", ForeignKey("transports.id")),
    Column("timeStart", DateTime),
    Column("timeEnd", DateTime, nullable=True),
    Column("priceOfUnit", Float),
    Column("priceType", OrmPriceType),
    Column("finalPrice", Float, nullable=True),
)


def start_mappers():
    accounts_mapper = mapper_registry.map_imperatively(Account, accounts)
    transport_mapper = mapper_registry.map_imperatively(
        Transport, transports, properties={"owner": relationship(Account)}
    )
    rent_mapper = mapper_registry.map_imperatively(
        Rent,
        rents,
        properties={
            "user": relationship(Account),
            "transport": relationship(Transport),
        },
    )
    return [accounts_mapper, transport_mapper, rent_mapper]
