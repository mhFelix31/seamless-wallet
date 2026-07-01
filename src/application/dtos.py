from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TransferDTO(BaseModel):
    receiver_id: str
    currency_code: str
    value: int


class ExternalTransferDTO(BaseModel):
    wallet_id: str
    currency_code: str
    value: int


class MoneyDTO(BaseModel):
    currency_code: str
    value: int


class TransactionResponseDTO(BaseModel):
    sender: str
    receiver: str
    amount: MoneyDTO
    balance: MoneyDTO
    uuid: UUID
    timestamp: datetime
