import time
from abc import ABC
from datetime import datetime, timezone
from typing import Tuple

import jwt

from framework.decorator import Decorator


class JwtSecurity(Decorator, ABC):
    def __init__(self, on_fail=lambda request, response: None):
        self._secret = "secret_key_temporary"
        self.on_fail = on_fail

    def secret(self):
        return self._secret


class JwtTokenFactory(JwtSecurity, ABC):
    def should_execute_endpoint(self, request, request_body) -> Tuple[bool, object]:
        if not self.verify_request(request, request_body):
            return False, None

        return True, jwt.encode({
            "username": request_body["username"].lower(),
            "exp": datetime.now(tz=timezone.utc).timestamp() + 60 * 30
        }, self.secret())

    def verify_request(self, request, request_body) -> bool:
        raise NotImplementedError(f"Must implement request verification for {type(self)}!")


class JwtTokenAuth(JwtSecurity):
    def should_execute_endpoint(self, request, request_body) -> Tuple[bool, object]:
        try:
            jwt.decode(request.headers["Authorization"][8:], self.secret(), algorithms=["HS256"])
            return True, None
        except:
            return False, None
