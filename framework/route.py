import re

from framework.http_method import HttpMethod
from framework.method import Method


class Route:
    VARIABLE_MATCHER = re.compile(r"({.+?})")  # Matches PathVariables. Matches string in url encased in {}
    SLASH_EXTRACTOR = re.compile(r"/?([^/]+)/?")  # extracts the strings between "/" separators in url

    def __init__(self, route: str, http_method: HttpMethod, func):
        """
        Every route in the framework has a specified route class which manages
        the matching of a url to a function.

        Firstly fixes the route url passed in into a standard url format for the framework
        which starts with a "/" and ends with a "/". if empty string then set to "/".
        :param route: the path of the function
        :param http_method: the method to access the route
        :param func: the function called
        """
        if len(route) == 0:
            route = "/"

        route = route if route[0] == "/" else "/" + route
        route = route if route[-1] == "/" else route + "/"

        self._route = route
        self._http_method = http_method
        self._func = func
        self._method = Method(self._func)

        self._variable_table = {i.group(): i.span() for i in self.VARIABLE_MATCHER.finditer(self._route)}
        self._route_contains_variables = len(self._variable_table) > 0
        self._route_slashes = self.SLASH_EXTRACTOR.findall(self._route)

    def matches_url(self, url):
        """
        Checks if a url matches the route.
        :param url: the url to check if it matches
        :return: True | False (Whether matches or not), path_variables | None (If there are any path variables, returns extracted)
        """

        if not self.has_route_variables():
            url = url if url[-1] == "/" else url + "/"
            return url == self._route

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
