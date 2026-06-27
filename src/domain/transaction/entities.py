from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.shared.money import Money
from src.domain.wallet.entities import Wallet

@dataclass(frozen=True)
class Transaction:
    source: Wallet
    receiver: Wallet

    amount: Money
    
    internal_id: int
    uuid: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
