import socket
import threading
import time

from framework.parser import RequestParser


class HttpClient:
    def __init__(self, client_socket: socket.socket, address, response_builder):
        self.socket = client_socket
        self.address = address
        self.response_builder = response_builder
        self.response_receive_time = 0
        self.is_closed = False
        self.response_handler_thread = threading.Thread(target=self.request_handler)

    def start(self):
        self.response_handler_thread.start()

    def close(self):
        self.socket.shutdown(socket.SHUT_WR)
        exit()

    def send(self, data: bytes):
        self.socket.send(data)

    def request_handler(self):
        while not self.is_closed:
            data: bytes = self.socket.recv(200)
            curr_data_buffer = data
            last_200 = False
            while len(curr_data_buffer) == 200 and not last_200:
                last_200 = len(self.socket.recv(201, socket.MSG_PEEK)) <= 200  # prevent blocking if next cycle has exactly 200
                curr_data_buffer = self.socket.recv(200)
                data += curr_data_buffer

            if len(data) < 12:
                continue

            request = RequestParser(data).parse()
            response = self.response_builder(request)
            response_data = response.data()
            self.send(response_data)
            self.close()
