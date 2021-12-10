import re

from framework.http import HttpMethod, ContentType, HttpRequest
from framework.method import Method


class Route:
    VARIABLE_MATCHER = re.compile(r"({.+?})")
    SLASH_EXTRACTOR = re.compile(r"/?([^/]+)/?")

    def __init__(self, route: str, http_method: HttpMethod, content_type: ContentType, func):
        if len(route) == 0:
            route = "/"

        route = route if route[0] == "/" else "/" + route
        route = route if route[-1] == "/" else route + "/"

        self._route = route
        self._http_method = http_method
        self._content_type = content_type
        self._func = func
        self._method = Method(self._func)

        self._variable_table = {i.group(): i.span() for i in self.VARIABLE_MATCHER.finditer(self._route)}
        self._route_contains_variables = len(self._variable_table) > 0
        self._route_slashes = self.SLASH_EXTRACTOR.findall(self._route)

    def execute(self, request: HttpRequest, response, path_variables):
        request.path_variables = path_variables
        return self._method.execute(request, response)

    def matches_url(self, url):
        if not self.has_route_variables():
            url = url if url[-1] == "/" else url + "/"
            url = url if url[0] == "/" else "/" + url
            return url == self._route, None

        variable_values = {}
        url_slashes = self.SLASH_EXTRACTOR.findall(url)

        if len(url_slashes) != len(self._route_slashes):
            return False, None

        for url_slash, route_slash in zip(url_slashes, self._route_slashes):
            if route_slash[0] != "{" and route_slash[-1] != "}":
                if url_slash != route_slash:
                    return False, None
            else:
                variable_values[route_slash[1:-1]] = url_slash

        return True, variable_values

    def has_route_variables(self):
        return self._route_contains_variables

    def route(self):
        return self._route

    def method(self):
        return self._http_method

    def content_type(self):
        return self._content_type

    def __str__(self):
        return f"Route(url: {self.route()})"
