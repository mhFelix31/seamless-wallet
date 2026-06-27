from copy import deepcopy
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from src.domain.currency.entities import Currency
from src.domain.shared.date_range import DateRange
from src.domain.shared.money import Money


@dataclass(frozen=True)
class Wallet:
    label: str
    uuid: UUID = field(default_factory=uuid4)
    is_external_managed: bool = False


@dataclass(frozen=True)
class WalletSnapshot:
    uuid: UUID = field(default_factory=uuid4)
    
    wallet: Wallet
    last_transaction_internal_id: int

    down_uuid: UUID | None
    down_balance: dict[Currency, Money] = field(default_factory=dict)

    snapshot_date_range: DateRange

    @property
    def balance(self) -> dict[Currency, Money]:
        cur_balance = deepcopy(self.down_balance)
        for transaction in self.transactions:
            cur_currency = transaction.amount.currency
            if cur_currency not in cur_balance.keys():
                cur_balance[cur_currency] = Money(currency=cur_currency, value=0)

            cur_balance[cur_currency] += transaction.amount
        return cur_balance
                

