from sqlalchemy import TypeDecorator, String

from simbir_go_backend.domain.model import PriceType, TransportType


class OrmPriceType(TypeDecorator):
    impl = String(255)
    cache_ok = True

    def process_bind_param(self, value: PriceType, dialect):
        return value.name

    def process_result_value(self, value: str, dialect):
        try:
            return PriceType(value)
        # We are probably getting 'RentType.<SomeType>' rather then just '<SomeType>' at this point
        # !Usually caused by tests!
        except ValueError:
            return PriceType(value.split(".")[-1])


class OrmTransportType(TypeDecorator):
    impl = String(255)
    cache_ok = True

    def process_bind_param(self, value: TransportType, dialect):
        return value.name

    def process_result_value(self, value: str, dialect):
        try:
            return TransportType(value)
        # We are probably getting 'TransportType.<SomeType>' rather then just '<SomeType>' at this point
        # !Usually caused by tests!
        except ValueError:
            return TransportType(value.split(".")[1])
