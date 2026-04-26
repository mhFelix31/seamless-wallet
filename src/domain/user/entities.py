from datetime import date
from uuid import UUID
from dataclasses import dataclass


@dataclass
class User:
    uuid: UUID
    email: str
    date_of_birth: date
    password_hash: str

    is_active: bool = True
