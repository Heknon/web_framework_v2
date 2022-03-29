import logging

from web_framework_v2.http import HttpRequest, ContentType
from web_framework_v2.http.http_method import HttpMethod
from web_framework_v2.http_server import HttpServer
from web_framework_v2.route import Endpoint
from web_framework_v2.route.endpoint import ErrorHandler
from web_framework_v2.route.endpoint_map import EndpointMap

logger = logging.getLogger(__name__)


class Framework:
    def __init__(
            self,
            static_folder: str,
            static_url_path: str,
            host: str = "localhost",
            port: int = 80,
            log_level=logging.INFO,
            error_handler: ErrorHandler = lambda exception, traceback, request, response, path_variables: {"error": str(exception),
                                                                                                           "traceback": traceback}
    ):
        logging.getLogger("web_framework_v2").setLevel(log_level)

        self._static_folder = static_folder
        self._static_url_path = static_url_path
        self._active = False
        self._error_handler = error_handler
        self._http_server = HttpServer(self, host, port)
        self._endpoint_map = EndpointMap()

    def start(self):
        self._active = True
        self._http_server.start()

    def get_endpoint(self, request: HttpRequest):
        return self._endpoint_map.get_endpoint(request)

    def add_endpoint(self, route: str, func, methods: {HttpMethod}, match_headers: dict, content_type: ContentType, error_handler: ErrorHandler):
        for method in methods:
            self._endpoint_map.add_route(Endpoint(route, method, content_type, func, match_headers, error_handler))

    def endpoint(
            self,
            route: str,
            methods: {HttpMethod} = None,
            content_type: ContentType = ContentType.json,
            match_headers: dict = None,
            error_handler: ErrorHandler = None
    ):
        assert route is not None and type(route) is str, "Route must be a valid string!"
        if error_handler is None:
            error_handler = self._error_handler

        if methods is None:
            methods = {HttpMethod.GET}

        if match_headers is None:
            match_headers = dict()

        if content_type is None:
            content_type = ContentType.json

        def decorator(f):
            self.add_endpoint(route, f, methods, match_headers, content_type, error_handler)
            return f

        return decorator

    def get(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.GET}, content_type, match_headers, error_handler)

    def post(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.POST}, content_type, match_headers, error_handler)

    def put(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.PUT}, content_type, match_headers, error_handler)

    def patch(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.PATCH}, content_type, match_headers, error_handler)

    def delete(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.DELETE}, content_type, match_headers, error_handler)

    def copy(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.COPY}, content_type, match_headers, error_handler)

    def head(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.HEAD}, content_type, match_headers, error_handler)

    def options(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.OPTIONS}, content_type, match_headers, error_handler)

    def link(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.LINK}, content_type, match_headers, error_handler)

    def unlink(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.UNLINK}, content_type, match_headers, error_handler)

    def purge(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.PURGE}, content_type, match_headers, error_handler)

    def lock(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.LOCK}, content_type, match_headers, error_handler)

    def unlock(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.UNLOCK}, content_type, match_headers, error_handler)

    def propfind(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.PROPFIND}, content_type, match_headers, error_handler)

    def view(
            self,
            route: str,
            match_headers: dict = None,
            content_type: ContentType = ContentType.json,
            error_handler: ErrorHandler = None
    ):
        return self.endpoint(route, {HttpMethod.VIEW}, content_type, match_headers, error_handler)

    def static_folder(self):
        return self._static_folder

    def static_url_path(self):
        return self._static_url_path

    def is_active(self):
        return self._active

    @property
    def error_handler(self):
        return self._error_handler
