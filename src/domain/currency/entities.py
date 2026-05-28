from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from src.domain.currency.exceptions import (
    CurrencyOutOfScaleException,
    InvalidCurrencyCodeException,
)


@dataclass(frozen=True)
class Currency:
    code: str
    scale: int

    def __post_init__(self):
        if len(self.code) > 5 or len(self.code) < 3:
            raise InvalidCurrencyCodeException()

        if self.scale < 0 or self.scale > 10:
            raise CurrencyOutOfScaleException()


@dataclass(frozen=True)
class ExchangeRate:
    base: Currency
    quote: Currency
    rate: Decimal  # base -> quote
    timestamp: datetime = field(default_factory=datetime.now)
