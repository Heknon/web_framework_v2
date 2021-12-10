from framework.http import HttpRequest, ContentType
from framework.http.http_method import HttpMethod
from framework.http_server import HttpServer
from framework.route import Route
from framework.route.route_map import RouteMap


class Framework:
    def __init__(self, static_folder: str, static_url_path: str):
        self._static_folder = static_folder
        self._static_url_path = static_url_path
        self._active = False
        self._http_server = HttpServer(self)
        self._route_map = RouteMap()

    def start(self):
        self._active = True
        self._http_server.start()

    def get_route(self, request: HttpRequest):
        return self._route_map.get_route(request.url, request.method)

    def add_route(self, route: str, func, methods: {HttpMethod}, content_type: ContentType = ContentType.json):
        for method in methods:
            self._route_map.add_route(Route(route, method, content_type, func))

    def route(self, route: str, methods: {HttpMethod} = None, content_type: ContentType = ContentType.json):
        if methods is None:
            methods = {HttpMethod.GET}

        def decorator(f):
            self.add_route(route, f, methods, content_type)

        return decorator

    def get(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.GET}, content_type)

    def post(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.POST}, content_type)

    def put(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.PUT}, content_type)

    def patch(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.PATCH}, content_type)

    def delete(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.DELETE}, content_type)

    def copy(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.COPY}, content_type)

    def head(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.HEAD}, content_type)

    def options(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.OPTIONS}, content_type)

    def link(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.LINK}, content_type)

    def unlink(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.UNLINK}, content_type)

    def purge(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.PURGE}, content_type)

    def lock(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.LOCK}, content_type)

    def unlock(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.UNLOCK}, content_type)

    def propfind(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.PROPFIND}, content_type)

    def view(self, route: str, content_type: ContentType = ContentType.json):
        return self.route(route, {HttpMethod.VIEW}, content_type)

    def static_folder(self):
        return self._static_folder

    def static_url_path(self):
        return self._static_url_path

    def is_active(self):
        return self._active
