from backend import app
from backend.token_factory import TokenFactory
from web_framework_v2 import RequestBody, QueryParameter, ContentType
from web_framework_v2.http import HttpStatus
from web_framework_v2.security.jwt import JwtTokenAuth


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
def test(request_body: RequestBody(parameter_type=int)):
    return request_body


@app.get("/calculate-area", content_type=ContentType.text)
def calc_area(width: QueryParameter("width", int), height: QueryParameter("height", int)):
    return width * height / 2


images = dict()


@app.post("/upload", content_type=ContentType.text)
def upload_image(name: QueryParameter("file-name"), data: RequestBody(raw_format=True)):
    images[name] = data
    return name


@app.get("/image", content_type=ContentType.jpg)
def get_image(name: QueryParameter("image-name")):
    print("test")
    return images[name]
