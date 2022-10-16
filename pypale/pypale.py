import random
import string
import time
from typing import Dict, List, Optional

import jwt
from black import Any


class Pypale:
    DEFAULT_JWT_ALGORITHM = "HS256"
    DEFAULT_ENCODING = "utf8"

    def __init__(
        self,
        token_ttl_minutes: int,
        base_url: str,
        secret_key: str,
        token_issue_ttl_seconds: int,
        jwt_algorithm: Optional[str] = None,
        encoding: Optional[str] = None,
    ):
        self.token_ttl_minutes = token_ttl_minutes
        self.base_url = base_url
        self.secret_key = secret_key
        self.token_issue_ttl_seconds = token_issue_ttl_seconds
        self.jwt_algorithm = jwt_algorithm or self.DEFAULT_JWT_ALGORITHM
        self.encoding = encoding or self.DEFAULT_ENCODING

    def generate_token(
        self, email: str, extras: Optional[Dict[str, Any]] = None
    ) -> str:
        if extras is not None:
            payload = self.generate_token_metadata(email=email, extras=extras)
        else:
            payload = self.generate_token_metadata(email=email)
        response = jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm=self.jwt_algorithm,
        )
        print(response)
        return response

    def generate_token_metadata(
        self,
        email: str,
        extras: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        result = {}
        if extras is not None:
            result.update(extras)
        result.update(
            {
                "sub": email,
                "jti": self.one_time_nonce(),
                "iat": int(time.time()),
                "exp": int(time.time()) + (self.token_ttl_minutes * 60),
                "iss": self.base_url,
            }
        )
        return result

    def one_time_nonce(
        self, size: int = 16, chars: str = string.ascii_letters + string.digits + "-"
    ) -> str:
        return "".join(random.choice(chars) for _ in range(size))

    def _token_is_expired(self, iat: int, token_issue_ttl_seconds: int) -> bool:
        return (iat + token_issue_ttl_seconds) < int(time.time())

    def valid_token(
        self,
        return_token: str = None,
        return_email: str = None,
        algorithms: Optional[List[str]] = None,
    ) -> bool:
        if algorithms is None:
            algorithms = [self.jwt_algorithm]
        if return_token is None:
            return False
        try:
            token_metadata = jwt.decode(
                return_token, self.secret_key, algorithms=algorithms
            )
        except jwt.exceptions.DecodeError:
            return False
        if self._token_is_expired(
            iat=token_metadata["iat"],
            token_issue_ttl_seconds=self.token_issue_ttl_seconds,
        ):
            return False

        if return_email is not None:
            if token_metadata["sub"] != return_email:
                return False
            return True
        else:
            return False

    def decode_token(
        self, token: str, key: str = None, algorithms: List[str] = None
    ) -> Dict:
        if key is None:
            key = self.secret_key
        if algorithms is None:
            algorithms = [self.jwt_algorithm]
        return jwt.decode(jwt=token, key=key, algorithms=algorithms)
