from .entities import User
from typing import Protocol


class UserRepository(Protocol):
    def save(self, user: User) -> bool: ...

    def get_by_email(self, email: str) -> User: ...
