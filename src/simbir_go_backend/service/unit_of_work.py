import abc
from simbir_go_backend.adapters.repository import (
    AbstractRentRepo,
    AbstractTransportRepo,
    AbstractAccountRepo,
    SqlAlchemyAccountRepo,
    SqlAlchemyRentRepo,
    SqlAlchemyTransportRepo,
)
from simbir_go_backend.config import get_postgres_uri, get_use_in_memory_database
from simbir_go_backend.adapters.sqlalchemy import orm

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


class AbstractUnitOfWork(abc.ABC):
    accounts: AbstractAccountRepo
    transport: AbstractTransportRepo
    rents: AbstractRentRepo

    def __exit__(self, *args):
        self.rollback()

    def __enter__(self, *args) -> "AbstractUnitOfWork":
        return self

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


engine = None

if not get_use_in_memory_database():
    engine = create_engine(
        get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )
else:
    engine = create_engine("sqlite://")
    
orm.metadata.create_all(bind=engine)
DEFAULT_SESSION_FACTORY = sessionmaker(bind=engine)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.accounts = SqlAlchemyAccountRepo(self.session)
        self.rents = SqlAlchemyRentRepo(self.session)
        self.transport = SqlAlchemyTransportRepo(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
