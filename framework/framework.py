from framework.http import HttpRequest, ContentType
from framework.http.http_method import HttpMethod
from framework.http_server import HttpServer
from framework.route import Endpoint
from framework.route.endpoint_map import EndpointMap


class Framework:
    def __init__(self, static_folder: str, static_url_path: str):
        self._static_folder = static_folder
        self._static_url_path = static_url_path
        self._active = False
        self._http_server = HttpServer(self)
        self._endpoint_map = EndpointMap()

    def start(self):
        self._active = True
        self._http_server.start()

    def get_endpoint(self, request: HttpRequest):
        return self._endpoint_map.get_endpoint(request.url, request.method)

    def add_endpoint(self, route: str, func, methods: {HttpMethod}, content_type: ContentType = ContentType.json):
        for method in methods:
            self._endpoint_map.add_route(Endpoint(route, method, content_type, func))

    def endpoint(self, route: str, methods: {HttpMethod} = None, content_type: ContentType = ContentType.json):
        if methods is None:
            methods = {HttpMethod.GET}

        def decorator(f):
            self.add_endpoint(route, f, methods, content_type)
            return f

        return decorator

    def get(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.GET}, content_type)

    def post(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.POST}, content_type)

    def put(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PUT}, content_type)

    def patch(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PATCH}, content_type)

    def delete(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.DELETE}, content_type)

    def copy(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.COPY}, content_type)

    def head(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.HEAD}, content_type)

    def options(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.OPTIONS}, content_type)

    def link(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.LINK}, content_type)

    def unlink(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.UNLINK}, content_type)

    def purge(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PURGE}, content_type)

    def lock(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.LOCK}, content_type)

    def unlock(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.UNLOCK}, content_type)

    def propfind(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.PROPFIND}, content_type)

    def view(self, route: str, content_type: ContentType = ContentType.json):
        return self.endpoint(route, {HttpMethod.VIEW}, content_type)

    def static_folder(self):
        return self._static_folder

    def static_url_path(self):
        return self._static_url_path

    def is_active(self):
        return self._active
