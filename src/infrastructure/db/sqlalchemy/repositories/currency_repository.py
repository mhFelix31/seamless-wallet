from datetime import datetime

from domain.currency.entities import Currency, ExchangeRate
from domain.currency.repository import CurrencyRepository, ExchangeRateRepository


class SQLAlchemyCurrencyRepository(CurrencyRepository):
    def __init__(self, session):
        self.session = session

    def save(self, cur: Currency) -> bool: ...

    def get_by_code(self, code: str) -> Currency: ...


class SQLAlchemyExchangeRateRepository(ExchangeRateRepository):
    def __init__(self, session):
        self.session = session

    def save(self, ex: ExchangeRate) -> bool: ...

    def get_latest_exchange_rate(self, cur: Currency) -> ExchangeRate: ...

    def get_rates_from_time_range(
        self, cur: Currency, start_datetime: datetime, end_datetime: datetime
    ) -> list[ExchangeRate]: ...
