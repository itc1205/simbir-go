import abc
from typing import List, Optional
from sqlalchemy import text, TextClause
from sqlalchemy.orm import Session

from simbir_go_backend.domain.model import Rent, Transport, Account
from enum import Enum


class SearchTransportType(str, Enum):
    Car = "Car"
    Bike = "Bike"
    Scooter = "Scooter"
    All = "All"


class AbstractAccountRepo(abc.ABC):
    def get(self, id: int) -> Optional[Account]:
        return self._get(id)

    def get_by_username(self, username: str) -> Optional[Account]:
        return self._get_by_username(username)

    def add(self, account: Account):
        return self._add(account)

    def delete(self, account: Account):
        return self._delete(account)

    def list(self, begin: int, limit: int) -> List[Account]:
        return self._list(begin, limit)

    @abc.abstractmethod
    def _delete(self, account: Account):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: int) -> Optional[Account]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_username(self, username: str) -> Optional[Account]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, account: Account):
        raise NotImplementedError

    @abc.abstractmethod
    def _list(self, begin: int, limit: int) -> List[Account]:
        raise NotImplementedError


class AbstractTransportRepo(abc.ABC):
    def get(self, id: int) -> Optional[Transport]:
        return self._get(id)

    def add(self, transport: Transport):
        return self._add(transport)

    def delete(self, transport: Transport):
        return self._delete(transport)

    def list(self, begin: int, limit: int) -> List[Transport]:
        return self._list(begin, limit)

    def list_closest(
        self,
        longitude: float,
        latitude: float,
        radius: float,
        transportType: SearchTransportType,
    ) -> List[Transport]:
        return self._list_closest(longitude, latitude, radius, transportType)

    @abc.abstractmethod
    def _delete(self, transport: Transport):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: int) -> Optional[Transport]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, transport: Transport):
        raise NotImplementedError

    @abc.abstractmethod
    def _list(self, begin: int, limit: int) -> List[Transport]:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_closest(
        self,
        longitude: float,
        latitude: float,
        radius: float,
        transportType: SearchTransportType,
    ) -> List[Transport]:
        raise NotImplementedError


class AbstractRentRepo(abc.ABC):
    def get(self, id: int) -> Optional[Rent]:
        return self._get(id)

    def add(self, rent: Rent):
        return self._add(rent)

    def delete(self, rent: Rent):
        return self._delete(rent)

    def list(self, begin: int, limit: int) -> List[Rent]:
        return self._list(begin, limit)

    def get_from_transport(self, id: int) -> List[Rent]:
        return self._get_from_transport(id)

    def get_from_user(self, id: int) -> List[Rent]:
        return self._get_from_user(id)

    @abc.abstractmethod
    def _get_from_transport(self, id: int) -> List[Rent]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_from_user(self, id: int) -> List[Rent]:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, rent: Rent):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: int) -> Optional[Rent]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, rent: Rent):
        raise NotImplementedError

    @abc.abstractmethod
    def _list(self, begin: int, limit: int) -> List[Rent]:
        raise NotImplementedError


class SqlAlchemyAccountRepo(AbstractAccountRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get(self, id: int) -> Optional[Account]:
        return self.session.query(Account).filter_by(id=id).one_or_none()

    def _get_by_username(self, username: str) -> Account | None:
        return self.session.query(Account).filter_by(username=username).one_or_none()

    def _add(self, account: Account):
        self.session.add(account)

    def _delete(self, account: Account):
        self.session.delete(account)

    def _list(self, begin: int, limit: int) -> List[Account]:
        return self.session.query(Account).offset(begin).limit(limit).all()


class SqlAlchemyTransportRepo(AbstractTransportRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _list_closest(
        self,
        longitude: float,
        latitude: float,
        radius: float,
        transportType: SearchTransportType,
    ) -> List[Transport]:
        result = self.session.execute(
            self.__build_closest_transport_query(
                longitude, latitude, radius, transportType
            )
        )

        transports = []

        for id, _distance in result:
            transport = self.session.query(Transport).get(id)
            transports.append(transport)

        return transports

    def _get(self, id: int) -> Optional[Transport]:
        return self.session.query(Transport).filter_by(id=id).one_or_none()

    def _add(self, transport: Transport):
        self.session.add(transport)

    def _delete(self, transport: Transport):
        self.session.delete(transport)

    def _list(self, begin: int, limit: int) -> List[Transport]:
        return self.session.query(Transport).offset(begin).limit(limit).all()

    @staticmethod
    def __build_closest_transport_query(
        longitude: float,
        latitude: float,
        radius: float,
        transportType: SearchTransportType,
    ) -> TextClause:
        query = (
            "SELECT t.id, v.distance "
            'FROM "Transports" t CROSS JOIN LATERAL '
            f"(VALUES ( 6371 * acos( cos( radians({latitude}) ) * cos( radians( t.latitude ) ) * cos( radians( t.longitude ) - radians({longitude}) ) + sin( radians({latitude}) ) * sin( radians( t.latitude ) ) ) "
            ")) v(distance) "
            f'WHERE v.distance < {radius} AND t."canBeRented"=True '
        )

        if not transportType == SearchTransportType.All:
            query += f"AND \"transportType\"='{transportType.value}' "

        query += "ORDER BY distance; "
        return text(query)


class SqlAlchemyRentRepo(AbstractRentRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get_from_user(self, id: int) -> List[Rent]:
        return self.session.query(Rent).filter_by(userId=id).all()

    def _get_from_transport(self, id: int) -> List[Rent]:
        return self.session.query(Rent).filter_by(transportId=id).all()

    def _get(self, id: int) -> Optional[Rent]:
        return self.session.query(Rent).filter_by(id=id).one_or_none()

    def _add(self, rent: Rent):
        self.session.add(rent)

    def _delete(self, rent: Rent):
        self.session.delete(rent)

    def _list(self, begin: int, limit: int) -> List[Rent]:
        return self.session.query(Rent).offset(begin).limit(limit).all()
