from typing import Protocol
from .entities import Wallet


class WalletRepository(Protocol):
    def save(self, wallet: Wallet) -> bool: ...
