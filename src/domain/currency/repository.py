from datetime import datetime
from typing import Protocol

from .entities import Currency, ExchangeRate


class CurrencyRepository(Protocol):
    def save(self, cur: Currency) -> bool: ...
    def get_by_code(self, code: str) -> Currency: ...


class ExchangeRateRepository(Protocol):
    def save(self, ex: ExchangeRate) -> bool: ...
    def get_latest_exchange_rate(self, cur: Currency) -> ExchangeRate: ...
    def get_rates_from_time_range(
        self, cur: Currency, start_datetime: datetime, end_datetime: datetime
    ) -> list[ExchangeRate]: ...
