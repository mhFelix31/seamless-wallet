from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class PasswordVerifyFailure(str, Enum):
    INVALID_CREDENTIALS = "invalid_credentials"
    INVALID_HASH = "invalid_hash"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True)
class PasswordHashResult:
    hashed_value: str
    success: bool = True
    exception: Exception | None = None


@dataclass(frozen=True)
class PasswordVerifyResult:
    success: bool
    reason: PasswordVerifyFailure | None = None
    exception: Exception | None = None


class BasePasswordHasher(ABC):
    def __init__(self, secret_pepper: str, stale_peppers: list[str] = []) -> None:
        self.pepper = secret_pepper
        self.stale_peppers = stale_peppers

    @abstractmethod
    def hash_value(self, raw_value: str) -> PasswordHashResult: ...

    @abstractmethod
    def verify_value(
        self, raw_value: str, hashed_value: str
    ) -> PasswordVerifyResult: ...
