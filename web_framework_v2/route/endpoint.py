import re
from typing import Callable, Dict

import web_framework_v2.http.http_request as http_request
import web_framework_v2.http.http_response as http_response
import web_framework_v2.method as method_module
from web_framework_v2.http import HttpMethod, ContentType

ErrorHandler = Callable[[Exception, str, http_request.HttpRequest, http_response.HttpResponse, Dict], object]


class Endpoint:
    VARIABLE_MATCHER = re.compile(r"({.+?})")
    SLASH_EXTRACTOR = re.compile(r"/?([^/]+)/?")

    def __init__(
            self,
            route: str,
            http_method: HttpMethod,
            content_type: ContentType,
            func, match_headers: dict,
            error_handler: ErrorHandler
    ):
        if len(route) == 0:
            route = "/"

        route = route if route[0] == "/" else "/" + route
        route = route if route[-1] == "/" else route + "/"

        self._route = route
        self._http_method = http_method
        self._content_type = content_type
        self._error_handler = \
            error_handler if error_handler is not None else lambda exception, traceback, request, response, path_variables: {"error": str(exception),
                                                                                                                             "traceback": traceback}
        self._func = func
        self._match_headers = match_headers
        self._method = method_module.Method(self._func)

        self._variable_table = {i.group(): i.span() for i in self.VARIABLE_MATCHER.finditer(self._route)}
        self._route_contains_variables = len(self._variable_table) > 0
        self._route_slashes = self.SLASH_EXTRACTOR.findall(self._route)

    def execute_error_handler(
            self,
            exception: Exception,
            traceback: str,
            request: http_request.HttpRequest,
            response: http_response.HttpResponse,
            path_variables: Dict
    ):
        return method_module.Method.encode_result(self._error_handler(exception, traceback, request, response, path_variables), response)

    def execute(self, request: http_request.HttpRequest, response, path_variables):
        request.path_variables = path_variables
        return self._method.execute(request, response)

    def matches_headers(self, request: http_request.HttpRequest):
        if self._match_headers is None or len(self._match_headers) == 0:
            return True

        request_headers = request.headers
        matches = True

        for header, value in self._match_headers.items():
            matches = header in request_headers and request_headers[header] == value

            if not matches:
                break

        return matches

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
