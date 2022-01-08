import logging

from web_framework_v2.http import HttpRequest, ContentType
from web_framework_v2.http.http_method import HttpMethod
from web_framework_v2.http_server import HttpServer
from web_framework_v2.route import Endpoint
from web_framework_v2.route.endpoint_map import EndpointMap

logger = logging.getLogger(__name__)


class Framework:
    def __init__(self, static_folder: str, static_url_path: str, host: str = "localhost", port: int = 80, log_level=logging.INFO):
        logging.getLogger("web_framework_v2").setLevel(log_level)

        self._static_folder = static_folder
        self._static_url_path = static_url_path
        self._active = False
        self._http_server = HttpServer(self, host, port)
        self._endpoint_map = EndpointMap()

    def start(self):
        self._active = True
        self._http_server.start()

    def get_endpoint(self, request: HttpRequest):
        return self._endpoint_map.get_endpoint(request)

    def add_endpoint(self, route: str, func, methods: {HttpMethod}, match_headers: dict, content_type: ContentType):
        for method in methods:
            self._endpoint_map.add_route(Endpoint(route, method, content_type, func, match_headers))

    def endpoint(self, route: str, methods: {HttpMethod} = None, content_type: ContentType = ContentType.json, match_headers: dict = None):
        assert route is not None and type(route) is str, "Route must be a valid string!"

        if methods is None:
            methods = {HttpMethod.GET}

        if match_headers is None:
            match_headers = dict()

        if content_type is None:
            content_type = ContentType.json

        def decorator(f):
            self.add_endpoint(route, f, methods, match_headers, content_type)
            return f

        return decorator

    def get(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.GET}, content_type, match_headers)

    def post(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.POST}, content_type, match_headers)

    def put(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PUT}, content_type, match_headers)

    def patch(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PATCH}, content_type, match_headers)

    def delete(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.DELETE}, content_type, match_headers)

    def copy(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.COPY}, content_type, match_headers)

    def head(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.HEAD}, content_type, match_headers)

    def options(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.OPTIONS}, content_type, match_headers)

    def link(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.LINK}, content_type, match_headers)

    def unlink(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.UNLINK}, content_type, match_headers)

    def purge(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PURGE}, content_type, match_headers)

    def lock(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.LOCK}, content_type, match_headers)

    def unlock(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.UNLOCK}, content_type, match_headers)

    def propfind(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PROPFIND}, content_type, match_headers)

    def view(self, route: str, match_headers: dict = None, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.VIEW}, content_type, match_headers)

    def static_folder(self):
        return self._static_folder

    def static_url_path(self):
        return self._static_url_path

    def is_active(self):
        return self._active
