import time
from abc import ABC
from datetime import datetime, timezone
from typing import Tuple

import jwt
from web_framework_v2.decorator import Decorator


class JwtSecurity(Decorator, ABC):
    _SECRET = "secret_key_temporary"

    def __init__(self, on_fail=lambda request, response: None, allow_access_on_error=False):
        """
        Base class of JWT security
        :param on_fail: called when security check fails.
        """
        self.on_fail = on_fail
        self.allow_access_on_error = allow_access_on_error

    @staticmethod
    def secret():
        return JwtSecurity._SECRET

    @staticmethod
    def set_secret(secret):
        JwtSecurity._SECRET = secret

    @staticmethod
    def decode_token(token):
        return jwt.decode(token, JwtSecurity.secret(), algorithms=["HS256"])

    @staticmethod
    def decode_request(request):
        return jwt.decode(request.headers["Authorization"][8:], JwtSecurity.secret(), algorithms=["HS256"])

    @staticmethod
    def create_token(self, data, expiration_seconds: int):
        data["exp"] = datetime.now(tz=timezone.utc).timestamp() + expiration_seconds
        return jwt.encode(data, JwtSecurity.secret())


class JwtTokenFactory(JwtSecurity, ABC):
    """
    Authenticates and creates a new token using request and request body
    """

    def __init__(self, on_fail=lambda request, response: None, allow_access_on_error=False, expiration_time=60 * 30):
        super().__init__(on_fail=on_fail, allow_access_on_error=allow_access_on_error)
        self.expiration_time = expiration_time

    def should_execute_endpoint(self, request, request_body) -> Tuple[bool, object, object]:
        authentication_result, fail_data = self.authenticate(request, request_body)
        if not authentication_result:
            return False, None, fail_data

        return True, JwtSecurity.create_token(self.token_data_builder(request, request_body), self.expiration_time), None

    def token_data_builder(self, request, request_body):
        raise NotImplementedError(f"Must implement token data builder for {type(self)}!")

    def authenticate(self, request, request_body) -> (bool, object):
        raise NotImplementedError(f"Must implement request authentication for {type(self)}!")


class JwtTokenAuth(JwtSecurity, ABC):
    """
    Allows access and authenticates using a pre-existing token.
    """

    def should_execute_endpoint(self, request, request_body) -> Tuple[bool, object, object]:
        authentication_result, fail_data = self.authenticate(request, request_body)
        try:
            return authentication_result, JwtSecurity.decode_request(request), fail_data
        except:
            try:
                return self.authenticate(request, request_body), None, fail_data
            except:
                return self.allow_access_on_error, None, fail_data

    def authenticate(self, request, request_body) -> (bool, object):
        raise NotImplementedError(f"Must implement authentication for {type(self)}!")
