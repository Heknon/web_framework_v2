from framework.framework import Framework
from framework.jwt import JwtTokenFactory, JwtTokenAuth

app = Framework("webroot", "/index.html")

user_db = {
    "heknon": "no"
}


class TokenFactory(JwtTokenFactory):
    def verify_request(self, request, request_body) -> bool:
        return request_body["username"].lower() in user_db and user_db[request_body["username"].lower()] == request_body["password"]


@TokenFactory()
@app.post("/register")
def register(token_factory_result: TokenFactory):
    return {
        "token": token_factory_result
    }


@JwtTokenAuth(on_fail=lambda request, response: "Failed to authenticate")
@app.post("/test")
def test():
    return "SUCCESS"


def main():
    app.start()


if __name__ == '__main__':
    main()
