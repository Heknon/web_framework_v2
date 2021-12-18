import inspect
import json

import jsonpickle
import jwt

from framework.annotations import RequestBody, QueryParameter, PathVariable
from framework.framework import Framework
from framework.http import HttpMethod, HttpRequest, ContentType
from framework.jwt import JwtSecurity

app = Framework("webroot", "/index.html")

images = {}


@app.route("/calculate-next", {HttpMethod.GET}, content_type=ContentType.text)
def calculate_next(num: QueryParameter("num", int)):
    return num + 1


@app.get("/calculate-area")
def calculate_area(height: QueryParameter("height", int), width: QueryParameter("width", int)):
    return height * width / 2


@app.get("/test")
@JwtSecurity.token_factory(

)
def test(req: HttpRequest):
    return "test"


@app.post("/upload", content_type=ContentType.text)
def upload(body: RequestBody(raw_format=True), name: QueryParameter("file-name")):
    images[name] = body
    return "SUCCESS!"


@app.get("/image", content_type=ContentType.jpg)
def get_image(name: QueryParameter("image-name")):
    return images.get(name, None)


def main():

    print(jwt.encode({"test": 2}, "SECRET"))
    print(jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZXN0IjoyfQ.hUggYjfZpywfbAilywls6Pj7PKKMrWwtdCo_u0liuT5", "SECRET", algorithms=["HS256"]))
    app.start()


if __name__ == '__main__':
    main()
