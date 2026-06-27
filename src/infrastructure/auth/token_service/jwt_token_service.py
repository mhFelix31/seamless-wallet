from dataclasses import asdict
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from .base import (
    BaseTokenService,
    TokenCreationResult,
    TokenPayload,
    TokenVerifyFailure,
    TokenVerifyResult,
)


class JWTTokenService(BaseTokenService):
    algorithm = "HS265"

    def create(self, user_uuid: str) -> TokenCreationResult:
        payload = TokenPayload(u=user_uuid)
        try:
            jwt_token = jwt.encode(
                asdict(payload), self.priv_token_key, algorithm=self.algorithm
            )
            result = TokenCreationResult(token=jwt_token)
        except Exception as ex:
            result = TokenCreationResult(token="", success=False, exception=ex)

        return result

    def verify(self, token: str) -> TokenVerifyResult:
        try:
            jwt_payload = jwt.decode(
                token, self.priv_token_key, algorithms=[self.algorithm]
            )
            result = TokenVerifyResult(payload=jwt_payload)
        except ExpiredSignatureError as ex:
            result = TokenVerifyResult(
                payload={}, reason=TokenVerifyFailure.EXPIRED_TOKEN, exception=ex
            )
        except InvalidSignatureError as ex:
            result = TokenVerifyResult(
                payload={}, reason=TokenVerifyFailure.INVALID_TOKEN, exception=ex
            )
        except Exception as ex:
            result = TokenVerifyResult(
                payload={}, reason=TokenVerifyFailure.INTERNAL_ERROR, exception=ex
            )

        return result
