from __future__ import annotations

from web_framework_v2.http import HttpMethod
from . import Route


class RouteMap:
    def __init__(self):
        self._method_routes_map = {}  # HttpMethod: {route_str: Route}

    def get_route(self, url: str, method: HttpMethod) -> tuple[Route | None, str | None] | None:
        route_obj = self._method_routes_map.get(method, {}).get(url, None)

        if route_obj is None:
            method_routes = self._method_routes_map.get(method, None)

            if method_routes is None:
                return route_obj, None

            for route in method_routes.values():
                matches, variable_map = route.matches_url(url)
                if matches:
                    return route, variable_map

        return route_obj, None

    def add_route(self, route: Route):
        assert self._method_routes_map.get(route.method(), {}).get(route.route(), None) is None, \
            "Route already exists! Cannot add existing route!"

        self._method_routes_map.setdefault(route.method(), {})
        self._method_routes_map[route.method()][route.route()] = route

    def __str__(self):
        return str(self._method_routes_map)
