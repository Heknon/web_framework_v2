import logging
import socket
import threading

from web_framework_v2.parser import RequestParser

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, client_socket: socket.socket, address, response_builder):
        self.socket = client_socket
        self.address = address
        self.response_builder = response_builder
        self.response_receive_time = 0
        self.is_closed = False
        self.response_handler_thread = threading.Thread(target=self.request_handler)
        self.byte_fetch_amount = 2048

    def start(self):
        self.response_handler_thread.start()

    def close(self):
        self.socket.shutdown(socket.SHUT_WR)
        logger.debug(f"Closing client socket and exiting client thread {threading.current_thread()}")
        exit()

    def send(self, data: bytes):
        self.socket.sendall(data)

    def request_handler(self):
        while not self.is_closed:
            data: bytes = self.socket.recv(self.byte_fetch_amount)
            curr_data_buffer = data
            last_bytes = False
            while len(curr_data_buffer) == self.byte_fetch_amount and not last_bytes:
                last_bytes = len(self.socket.recv(self.byte_fetch_amount + 1,
                                                  socket.MSG_PEEK)) <= self.byte_fetch_amount  # prevent blocking if cycle equals fetch amount
                curr_data_buffer = self.socket.recv(self.byte_fetch_amount)
                data += curr_data_buffer

            request = RequestParser(data).parse()
            logger.debug(f"Finished building request object {request}")
            response = self.response_builder(request)
            logger.debug(f"Finished building response object {response}")
            response_data = response.data()
            self.send(response_data)
            self.close()
