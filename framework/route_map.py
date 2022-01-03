from framework.http_method import HttpMethod
from framework.route import Route


class RouteMap:
    def __init__(self):
        """
        Manages framework routes.
        Tracks the creation of routes
        Safely gets routes from the map
        """
        self._method_routes_map = {}  # HttpMethod: {route_str: Route}

    def get_route(self, route: str, method: HttpMethod):
        return self._method_routes_map.get(method, {}).get(route, None)

    def add_route(self, route: Route):
        assert self._method_routes_map.get(route.method(), {}).get(route.route(), None) is None, \
            "Route already exists! Cannot add existing route!"

        self._method_routes_map.setdefault(route.method(), {})
        self._method_routes_map[route.method()][route.route()] = route

    def __str__(self):
        return str(self._method_routes_map)
