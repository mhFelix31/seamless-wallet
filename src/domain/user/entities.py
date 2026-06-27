from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.enums import Role


@dataclass
class User:
    uuid: UUID
    full_name: str
    email: str
    date_of_birth: date
    password_hash: str
    role: Role

    is_active: bool = True
