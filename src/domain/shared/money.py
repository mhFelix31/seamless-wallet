from dataclasses import dataclass
from decimal import Decimal

from src.domain.currency.entities import Currency
from src.domain.shared.exception import (
    DifferentCurrenciesException,
    NotAddingWithMoneyException,
)


@dataclass
class Money:
    currency: Currency
    value: int

    @classmethod
    def from_input(cls, currency: Currency, entry_value: Decimal) -> "Money":
        multiplier = 10**currency.scale
        normalized = int(entry_value * multiplier)
        return cls(currency=currency, value=normalized)

    @property
    def decimal_value(self):
        if self.value == 0:
            return Decimal(0)

        multiplier = 10**self.currency.scale
        return Decimal(self.value) / Decimal(multiplier)

    def _ensure_same_currency(self, other: "Money"):
        if self.currency.code != other.currency.code:
            raise DifferentCurrenciesException()

    def _ensure_same_type(self, other):
        if not isinstance(other, Money):
            raise NotAddingWithMoneyException()

    def __add__(self, other: "Money"):
        self._ensure_same_type(other)
        self._ensure_same_currency(other)

        result = self.value + other.value
        return Money(currency=self.currency, value=result)

    def __radd__(self, other):
        self._ensure_same_type(other)
        self._ensure_same_currency(other)

        if other.value == 0:
            return self
        return self.__add__(other)
