from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum


class TokenVerifyFailure(str, Enum):
    INVALID_TOKEN = "invalid_token"
    EXPIRED_TOKEN = "expired_token"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True)
class TokenCreationResult:
    token: str
    success: bool = True
    exception: Exception | None = None


@dataclass(frozen=True)
class TokenVerifyResult:
    payload: dict
    reason: TokenVerifyFailure | None = None
    exception: Exception | None = None


@dataclass
class TokenPayload:
    u: str  # User
    exp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1)
    )  # Expiration


@dataclass(frozen=True)
class EnvTokens:
    env_label: str
    public_token: str


class BaseTokenService(ABC):
    def __init__(self, priv_token_key, env_token_pub_list: list[EnvTokens]):
        self.priv_token_key = priv_token_key
        self.env_token_pub_list = env_token_pub_list

    @abstractmethod
    def create(self, user_uuid: str) -> TokenCreationResult: ...

    @abstractmethod
    def verify(self, token: str) -> TokenVerifyResult: ...
