import base64
import logging
import random
import string
import time
from typing import Dict

import jwt


class Pypale:
    JWT_ALGORITHM = "HS256"
    ENCODING = "utf8"

    def __init__(
        self,
        token_ttl_minutes: int,
        base_url: str,
        secret_key: str,
        token_issue_ttl_seconds: int,
    ):
        self.token_ttl_minutes = token_ttl_minutes
        self.base_url = base_url
        self.secret_key = secret_key
        self.token_issue_ttl_seconds = token_issue_ttl_seconds

    def generate_token(self, email: str) -> str:
        return base64.b64encode(
            jwt.encode(
                payload=self.generate_token_metadata(email),
                key=self.secret_key,
                algorithm=self.JWT_ALGORITHM,
            ).encode(self.ENCODING)
        ).decode(self.ENCODING)

    def generate_token_metadata(self, email: str) -> Dict:
        return {
            "sub": email,
            "jti": self.one_time_nonce(),
            "iat": int(time.time()),
            "exp": int(time.time()) + (self.token_ttl_minutes * 60),
            "iss": self.base_url,
        }

    def one_time_nonce(
        self, size: int = 16, chars: str = string.ascii_letters + string.digits + "-"
    ) -> str:
        return "".join(random.choice(chars) for _ in range(size))

    def _token_is_expired(self, iat: int, token_issue_ttl_seconds: int) -> bool:
        return (iat + token_issue_ttl_seconds) < int(time.time())

    def valid_token(self, return_token: str = None, return_email: str = None) -> bool:
        if return_token is None:
            raise ValueError("return_token was not specified")
        decoded_return_token = base64.b64decode(return_token).decode(self.ENCODING)
        token_metadata = jwt.decode(
            decoded_return_token, self.secret_key, algorithms=[self.JWT_ALGORITHM]
        )
        if self._token_is_expired(
            iat=token_metadata["iat"],
            token_issue_ttl_seconds=self.token_issue_ttl_seconds,
        ):
            logging.warning("Token was issued too long ago.")
            return False

        if return_email is not None:
            if token_metadata["sub"] != return_email:
                logging.warning("Token is not issued to the right user.")
                return False
            return True
        else:
            logging.warning("Return email was not specified.")
            return False
