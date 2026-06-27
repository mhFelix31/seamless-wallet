from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .base import (
    BasePasswordHasher,
    PasswordHashResult,
    PasswordVerifyFailure,
    PasswordVerifyResult,
)


class Argon2PasswordHasher(BasePasswordHasher):
    def __init__(
        self, secret_pepper: str, stale_peppers: list[str] = [], *args, **kwargs
    ) -> None:
        super().__init__(
            secret_pepper=secret_pepper,
            stale_peppers=stale_peppers,
            *args,
            **kwargs,
        )
        self.password_hasher = PasswordHasher()

    def hash_value(self, raw_value: str) -> PasswordHashResult:
        try:
            hashed_value = self.password_hasher.hash(raw_value + self.pepper)
            result = PasswordHashResult(hashed_value=hashed_value)
        except Exception as ex:
            result = PasswordHashResult(hashed_value="", success=False, exception=ex)

        return result

    def verify_value(self, raw_value: str, hashed_value: str) -> PasswordVerifyResult:
        try:
            self.password_hasher.verify(hashed_value, raw_value + self.pepper)
            result = PasswordVerifyResult(success=True)
        except VerifyMismatchError as ex:
            result = PasswordVerifyResult(
                success=False,
                reason=PasswordVerifyFailure.INVALID_CREDENTIALS,
                exception=ex,
            )
        except Exception as ex:
            result = PasswordVerifyResult(
                success=False, reason=PasswordVerifyFailure.INTERNAL_ERROR, exception=ex
            )

        return result
