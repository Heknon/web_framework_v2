from abc import ABC
from datetime import datetime, timezone
from typing import Tuple

import jwt

from web_framework_v2.decorator import Decorator
from web_framework_v2.security import KeyPair


class JwtSecurity(Decorator, ABC):
    access_key: KeyPair
    refresh_key: KeyPair

    def __init__(self, on_fail=lambda request, response: None, fail_on_null_result=True):
        """
        Base class of JWT security
        :param on_fail: called when security check fails.
        """
        super().__init__(fail_on_null_result)
        self.on_fail = on_fail

    @staticmethod
    def access_key() -> KeyPair:
        return JwtSecurity.access_key

    @staticmethod
    def refresh_key() -> KeyPair:
        return JwtSecurity.refresh_key

    @staticmethod
    def set_access_key(key: KeyPair):
        JwtSecurity.access_key = key

    @staticmethod
    def set_refresh_key(key: KeyPair):
        JwtSecurity.refresh_key = key

    @staticmethod
    def _decode_token(token: str, key: KeyPair):
        try:
            return jwt.decode(token, key.public, algorithms=["RS256"])
        except:
            return None

    @staticmethod
    def _create_token(data, expiration_seconds: int, key: KeyPair):
        data["exp"] = int(datetime.now(tz=timezone.utc).timestamp() + expiration_seconds)
        return jwt.encode(data, key.private, algorithm='RS256')

    @staticmethod
    def decode_request(request):
        return JwtSecurity.decode_access_token(request.headers["authorization"][8:]) if "authorization" in request.headers \
                                                                                        and len(request.headers["authorization"]) > 8 else None

    @staticmethod
    def decode_refresh_token(token: str):
        return JwtSecurity._decode_token(token, JwtSecurity.refresh_key)

    @staticmethod
    def decode_access_token(token: str):
        return JwtSecurity._decode_token(token, JwtSecurity.access_key)

    @staticmethod
    def create_refresh_token(data, expiration_seconds: int):
        return JwtSecurity._create_token(data, expiration_seconds, JwtSecurity.refresh_key)

    @staticmethod
    def create_access_token(data, expiration_seconds: int):
        return JwtSecurity._create_token(data, expiration_seconds, JwtSecurity.access_key)


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

        return True, JwtSecurity.create_access_token(self.token_data_builder(request, request_body, builder_data), self.expiration_time), authentication_data

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
