
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Wallet():
    name: str
    uuid: UUID = field(default_factory=uuid4)
    