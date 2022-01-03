from web_framework_v2.http import HttpMethod


class HttpRequest:
    def __init__(self, http_method: HttpMethod, url: str, version: str, headers: dict, query_parameters: dict, body: bytes, path_variables=None):
        self.method = http_method
        self.url: str = url
        self.http_version: str = version
        self.headers = headers if headers is not None else {}
        self.query_parameters = query_parameters if query_parameters is not None else {}
        self.body = body
        self.path_variables = path_variables

    def get_header(self, name: str):
        return self.headers.get(name, None)

    def get_query_parameter(self, name: str):
        return self.query_parameters.get(name, None)

    def clone(self):
        return HttpRequest(
            self.method,
            self.url,
            self.http_version,
            dict(self.headers) if self.headers is not None else None,
            dict(self.query_parameters) if self.query_parameters is not None else None,
            self.body,
            self.path_variables
        )

    def __str__(self):
        return f"HttpRequest(method: {self.method}, url: {self.url}, http_version: {self.http_version}, headers: {self.headers}, query_parameters: {self.query_parameters}"
