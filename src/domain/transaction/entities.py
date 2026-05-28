from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.shared.money import Money

# MAYBE
# class Entry:
#    wallet_id: UUID
#    amount: Money

# class Transaction:
#    id: UUID
#    entries: list[Entry]
# ENDMAYBE


@dataclass(frozen=True)
class Transaction:
    source_uuid: UUID
    receiver_uuid: UUID

    amount: Money

    uuid: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
