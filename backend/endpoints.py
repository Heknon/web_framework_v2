from backend import app
from backend.token_factory import TokenFactory
from framework.http import HttpStatus
from framework.jwt import JwtTokenAuth


def on_fail(req, res):
    res.status = HttpStatus.UNAUTHORIZED
    return "Unauthorized"


@TokenFactory(on_fail=on_fail)
@app.post("/register")
def register(token_factory_result: TokenFactory):
    return {
        "token": token_factory_result
    }


@JwtTokenAuth(on_fail=on_fail)
@app.get("/test", match_headers={"Host": "business_name.localhost"})
def test(token: JwtTokenAuth):
    return token
