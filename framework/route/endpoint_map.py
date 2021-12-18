from __future__ import annotations

from framework.http import HttpMethod
from . import Endpoint


class EndpointMap:
    def __init__(self):
        self._method_routes_map = {}  # HttpMethod: {route_str: Route}

    def get_endpoint(self, url: str, method: HttpMethod) -> tuple[Endpoint | None, str | None] | None:
        endpoint_obj = self._method_routes_map.get(method, {}).get(url, None)

        if endpoint_obj is None:
            method_routes = self._method_routes_map.get(method, None)

            if method_routes is None:
                return endpoint_obj, None

            for route in method_routes.values():
                matches, variable_map = route.matches_url(url)
                if matches:
                    return route, variable_map

        return endpoint_obj, None

    def add_route(self, route: Endpoint):
        assert self._method_routes_map.get(route.method(), {}).get(route.route(), None) is None, \
            "Route already exists! Cannot add existing route!"

        self._method_routes_map.setdefault(route.method(), {})
        self._method_routes_map[route.method()][route.route()] = route

    def __str__(self):
        return str(self._method_routes_map)
