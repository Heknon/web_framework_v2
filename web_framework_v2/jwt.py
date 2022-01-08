import time
from abc import ABC
from datetime import datetime, timezone
from typing import Tuple

import jwt
from web_framework_v2.decorator import Decorator


class JwtSecurity(Decorator, ABC):
    _SECRET = "secret_key_temporary"

    def __init__(self, on_fail=lambda request, response: None):
        """
        Base class of JWT security
        :param on_fail: called when security check fails.
        """
        self.on_fail = on_fail

    @staticmethod
    def secret():
        return JwtSecurity._SECRET

    @staticmethod
    def set_secret(secret):
        JwtSecurity._SECRET = secret

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, JwtSecurity.secret(), algorithms=["HS256"])
        except:
            return None

    @staticmethod
    def decode_request(request):
        return JwtSecurity.decode_token(request.headers["Authorization"][8:]) if "Authorization" in request.headers else None

    @staticmethod
    def create_token(data, expiration_seconds: int):
        data["exp"] = datetime.now(tz=timezone.utc).timestamp() + expiration_seconds
        return jwt.encode(data, JwtSecurity.secret())


class JwtTokenFactory(JwtSecurity, ABC):
    """
    Authenticates and creates a new token using request and request body
    """

    def __init__(self, on_fail=lambda request, response: None, expiration_time=60 * 30):
        super().__init__(on_fail=on_fail)
        self.expiration_time = expiration_time

    def should_execute_endpoint(self, request, request_body) -> Tuple[bool, object, object]:
        authentication_result, authentication_data, builder_data = self.authenticate(request, request_body)
        if not authentication_result:
            return False, None, authentication_data

        return True, JwtSecurity.create_token(self.token_data_builder(request, request_body, builder_data), self.expiration_time), authentication_data

    def token_data_builder(self, request, request_body, data):
        raise NotImplementedError(f"Must implement token data builder for {type(self)}!")

    def authenticate(self, request, request_body) -> (bool, object):
        raise NotImplementedError(f"Must implement request authentication for {type(self)}!")


class JwtTokenAuth(JwtSecurity, ABC):
    """
    Allows access and authenticates using a pre-existing token.
    """

    def should_execute_endpoint(self, request, request_body) -> Tuple[bool, object, object]:
        decoded_token = JwtSecurity.decode_request(request)
        authentication_result, authentication_data = self.authenticate(request, request_body, decoded_token)

        return authentication_result, self.decoded_token_transformer(request, request_body, decoded_token), authentication_data

    def authenticate(self, request, request_body, decoded_token) -> (bool, object):
        raise NotImplementedError(f"Must implement authentication for {type(self)}!")

    def decoded_token_transformer(self, request, request_body, decoded_token) -> (bool, object):
        raise NotImplementedError(f"Must implement decoded_token_transformer for {type(self)}!")