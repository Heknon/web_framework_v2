from __future__ import annotations

from . import Endpoint
import web_framework_v2.http.http_request as http_request


class EndpointMap:
    def __init__(self):
        self._method_routes_map = {}  # HttpMethod: {route_str: Route}

    def get_endpoint(self, request: http_request.HttpRequest) -> tuple[Endpoint | None, str | None] | None:
        endpoint_obj = self._method_routes_map.get(request.method, {}).get(request.url, None)

        if endpoint_obj is None:
            method_routes = self._method_routes_map.get(request.method, None)

            if method_routes is None:
                return None, None

            for route in method_routes.values():
                matches, variable_map = route.matches_url(request.url)
                if matches and route.matches_headers(request):
                    return route, variable_map

        if endpoint_obj is not None and not endpoint_obj.matches_headers(request):
            return None, None

        return endpoint_obj, None

    def add_route(self, route: Endpoint):
        assert self._method_routes_map.get(route.method(), {}).get(route.route(), None) is None, \
            "Route already exists! Cannot add existing route!"

        self._method_routes_map.setdefault(route.method(), {})
        self._method_routes_map[route.method()][route.route()] = route

    def __str__(self):
        return str(self._method_routes_map)
