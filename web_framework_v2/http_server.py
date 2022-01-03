import socket
import ssl
import threading

from web_framework_v2.http import HttpResponse
from web_framework_v2.http_client import HttpClient

class HttpServer:
    def __init__(self, framework):
        self._framework = framework
        self._ip = ("0.0.0.0", 80)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_listen_thread = threading.Thread(target=self.__client_listener)

    def start(self):
        self._socket.bind(self._ip)
        self._socket.listen(2)
        self._client_listen_thread.start()
        print("The server is active and listening...")

    def __client_listener(self):
        while self._framework.is_active():
            client_socket, address = self._socket.accept()
            client = HttpClient(client_socket, address, lambda req: self.response_builder(req))
            client.start()

        self.shutdown()

    def response_builder(self, request):
        route, path_variables = self._framework.get_endpoint(request)

        if route is not None:
            return HttpResponse.build_from_route(request, route, path_variables)
        else:
            path = self._framework.static_folder() + (self._framework.static_url_path() if request.url == "/" else request.url)
            return HttpResponse.build_from_file(request, path)

    def shutdown(self):
        self._socket.shutdown(socket.SHUT_WR)
