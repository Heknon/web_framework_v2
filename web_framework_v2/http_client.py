import logging
import socket
import threading
from typing import Optional

from web_framework_v2.parser import RequestParser
from web_framework_v2.restartable_timer import RestartableTimer

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, client_socket: socket.socket, address, response_builder):
        self.socket = client_socket
        self.address = address
        self.response_builder = response_builder
        self.response_receive_time = 0
        self.is_closed = False
        self.response_handler_thread = threading.Thread(target=self.request_handler)
        self.byte_fetch_amount = 1024 * 8
        self.default_keep_alive_timeout = 10
        self.keep_alive_timer: Optional[RestartableTimer] = None
        self.connection_count = 0
        self.in_session = False

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
            if data == '':  # received FIN close socket.
                return self.close()

            if self.keep_alive_timer is not None:
                self.keep_alive_timer.reset()

            request_parser: RequestParser
            split_at_2crlf = data.split(b'\r\n\r\n')
            self.connection_count += 1

            while len(split_at_2crlf) != 2:
                fetched = self.socket.recv(self.byte_fetch_amount)
                if fetched == '':  # received FIN close socket.
                    return self.close()

                data += fetched
                split_at_2crlf = fetched.split(b'\r\n\r\n')

            request_parser = RequestParser(data)
            request = request_parser.parse()
            body_data = split_at_2crlf[1]

            missingData = int(request.headers.get("content-length", 0)) - len(request.body) - len(body_data)
            missingCounter = missingData
            while missingCounter > 0:
                fetch_amount = max(0, min(self.byte_fetch_amount, missingCounter))
                fetched_data = self.socket.recv(fetch_amount)
                if fetched_data == '':  # received FIN close socket.
                    return self.close()

                body_data += fetched_data
                missingCounter -= len(fetched_data)

            request.body = body_data

            logger.debug(f"Finished building request object {request}")
            response = self.response_builder(request)
            logger.debug(f"Finished building response object {response}")
            response_data = response.data()
            self.send(response_data)

            if 'keep-alive' in request.headers:
                keep_alive = HttpClient.parse_header_for_parameters(request.headers['keep-alive'])

                if not self.in_session:
                    timeout: int
                    try:
                        timeout = int(keep_alive['timeout']) if 'timeout' in keep_alive else self.default_keep_alive_timeout
                    except:
                        timeout = self.default_keep_alive_timeout

                    self.keep_alive_timer = RestartableTimer(timeout, self.keep_alive_timeout)
                    self.keep_alive_timer.run()
                    self.in_session = True

            if 'connection' in request.headers:
                connection = request.headers['connection'].lower().strip()
                if connection == 'keep-alive' and not self.in_session:
                    print('started session')
                    self.keep_alive_timer = RestartableTimer(self.default_keep_alive_timeout, self.keep_alive_timeout)
                    self.keep_alive_timer.run()
                    self.in_session = True

            if self.in_session:
                continue

            self.close()

    @staticmethod
    def parse_header_for_parameters(header) -> dict:
        cursor = 0
        parameters = {}

        current_parameter_name = ""
        while cursor < len(header):
            curr = header[cursor]

            if curr == '=':
                parameters[current_parameter_name] = ""
            elif curr == ',':
                cursor += 1
                while cursor < len(header) and header[cursor] == ' ':
                    cursor += 1
            elif current_parameter_name not in parameters:
                current_parameter_name += curr
            elif current_parameter_name in parameters:
                parameters[current_parameter_name] += curr

            cursor += 1

        return parameters

    def keep_alive_timeout(self):
        self.keep_alive_timer.cancel()
        self.keep_alive_timer = None
        self.close()

