from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from simbir_go_backend.adapters.sqlalchemy import orm
from simbir_go_backend.service.unit_of_work import SqlAlchemyUnitOfWork
from simbir_go_backend.config import (
    get_use_in_memory_database,
    get_postgres_uri,
)


def get_uow():
    engine = None

    if not get_use_in_memory_database():
        engine = create_engine(
            get_postgres_uri(),
        )
    else:
        engine = create_engine("sqlite:///sqlite.db")

    orm.metadata.create_all(bind=engine)
    sessionFactory = sessionmaker(bind=engine)

    uow = SqlAlchemyUnitOfWork(sessionFactory)
    yield uow
