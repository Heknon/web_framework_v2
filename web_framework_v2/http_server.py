import logging
import socket
import threading

from web_framework_v2.http import HttpResponse
from web_framework_v2.http_client import HttpClient

logger = logging.getLogger(__name__)


class HttpServer:
    def __init__(self, framework, host, port):
        self._framework = framework
        self._ip = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_listen_thread = threading.Thread(target=self.__client_listener)

    def start(self):
        self._socket.bind(self._ip)
        self._socket.listen(2)
        self._client_listen_thread.start()
        logger.info("The server is active and listening...")

    def __client_listener(self):
        while self._framework.is_active():
            client_socket, address = self._socket.accept()
            logger.debug(f"Accepted client connection from {address}")
            client = HttpClient(client_socket, address, lambda req: self.response_builder(req))
            client.start()

        self.shutdown()

    def response_builder(self, request):
        logger.debug(f"Attempting to find a endpoint using {request.url}")
        route, path_variables = self._framework.get_endpoint(request)

        if route is not None:
            logger.debug(f"Found route {route}")
            return HttpResponse.build_from_route(request, route, path_variables, self._framework.error_handler)
        else:
            logger.debug("Failed to find endpoint, building response using static folder.")
            path = self._framework.static_folder() + (self._framework.static_url_path() if request.url == "/" else request.url)
            return HttpResponse.build_from_file(request, path)

    def shutdown(self):
        self._socket.shutdown(socket.SHUT_WR)
        exit(0)
