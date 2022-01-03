from web_framework_v2.jwt import JwtTokenFactory

user_db = {
    "heknon": "no"
}


class TokenFactory(JwtTokenFactory):
    def verify_request(self, request, request_body) -> bool:
        return request_body["username"].lower() in user_db and user_db[request_body["username"].lower()] == request_body["password"]