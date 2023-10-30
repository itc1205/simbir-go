import abc
from typing import List, Optional
from sqlalchemy.orm import Session

from simbir_go_backend.domain.model import Rent, Transport, Account


class AbstractAccountRepo(abc.ABC):
    def get(self, id: int) -> Optional[Account]:
        return self._get(id)

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


class AbstractRentRepo(abc.ABC):
    def get(self, id: int) -> Optional[Rent]:
        return self._get(id)

    def add(self, rent: Rent):
        return self._add(rent)

    def delete(self, rent: Rent):
        return self._delete(rent)

    def list(self, begin: int, limit: int) -> List[Rent]:
        return self._list(begin, limit)

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

    def _add(self, account: Account):
        self.session.add(account)

    def _delete(self, account: Account):
        self.session.delete(account)

    def _list(self, begin: int, limit: int) -> List[Account]:
        return self.session.query(Account).offset(begin).limit(limit).all()


class SqlAlchemyTransportRepo(AbstractTransportRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get(self, id: int) -> Optional[Transport]:
        return self.session.query(Transport).filter_by(id=id).one_or_none()

    def _add(self, transport: Transport):
        self.session.add(transport)

    def _delete(self, transport: Transport):
        self.session.delete(transport)

    def _list(self, begin: int, limit: int) -> List[Transport]:
        return self.session.query(Transport).offset(begin).limit(limit).all()


class SqlAlchemyRentRepo(AbstractRentRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get(self, id: int) -> Optional[Rent]:
        return self.session.query(Rent).filter_by(id=id).one_or_none()

    def _add(self, rent: Rent):
        self.session.add(rent)

    def _delete(self, rent: Rent):
        self.session.delete(rent)

    def _list(self, begin: int, limit: int) -> List[Rent]:
        return self.session.query(Rent).offset(begin).limit(limit).all()
