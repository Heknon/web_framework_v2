import inspect
import json

import jsonpickle

from framework.annotations import RequestBody, QueryParameter, PathVariable
from framework.framework import Framework
from framework.http import HttpMethod, HttpRequest, ContentType

app = Framework("webroot", "/index.html")

images = {}


@app.route("/calculate-next", {HttpMethod.GET}, content_type=ContentType.text)
def calculate_next(num: QueryParameter("num", int)):
    return num + 1


@app.get("/calculate-area")
def calculate_area(height: QueryParameter("height", int), width: QueryParameter("width", int)):
    return height * width / 2

@app.get("/test")
def test():
    return "test"


@app.post("/upload", content_type=ContentType.text)
def upload(body: RequestBody(raw_format=True), name: QueryParameter("file-name")):
    images[name] = body
    return "SUCCESS!"


@app.get("/image", content_type=ContentType.jpg)
def get_image(name: QueryParameter("image-name")):
    return images.get(name, None)


def main():
    app.start()


if __name__ == '__main__':
    main()
