from web_framework_v2.http import HttpMethod, HttpRequest


class RequestParser:
    def __init__(self, request: bytes):
        """
        Efficiently parses a request into a HttpRequest object.
        :param request: the HTTP request received from the browser
        """

        self.request = request
        self.length = len(self.request)
        self.cursor = 0

    def parse(self):
        try:
            method = HttpMethod.__getitem__(self.extract_till_space())
            url, query_parameters = self.parse_url()
            version = self.extract_till_carriage()
            headers = self.parse_header_space()
            self.skip_carriage()
            body = self.request[self.cursor:]

            return HttpRequest(method, url, version, headers, query_parameters, body)
        except:
            print("ERROR:")
            print(self.request)
            print("=-=-=-=-= ERROR =-=-=-=-=")
            raise

    def current(self):
        if self.cursor >= self.length:
            return None
        return chr(self.request[self.cursor])

    def next(self):
        if self.cursor + 1 >= self.length:
            return None
        return chr(self.request[self.cursor + 1])

    def parse_url(self):
        url_buffer = ""
        query_parameters = {}

        while self.current() != "?" and self.current() != " ":
            url_buffer += self.current()
            self.cursor += 1

        if self.current() != "?":
            return url_buffer, None

        self.cursor += 1
        curr_name = ""
        searching_name = True
        while self.current() != " ":
            curr = self.current()
            if curr == "&":
                searching_name = True
                if curr_name not in query_parameters and curr_name != "":
                    query_parameters[curr_name] = None
                curr_name = ""
                self.cursor += 1
                continue
            elif curr == "=":
                searching_name = False
                self.cursor += 1
                continue

            if searching_name:
                curr_name += curr
                self.cursor += 1
            else:
                values_str = ""
                while self.current() != "&" and self.current() != " ":
                    values_str += self.current()
                    self.cursor += 1
                curr_value = values_str.split(",")
                query_parameters[curr_name] = curr_value

        if curr_name not in query_parameters:
            query_parameters[curr_name] = None
        self.cursor += 1
        return url_buffer, query_parameters

    def parse_header_space(self):
        headers = {}

        while self.skip_carriage() < 2:
            header = self.extract_till_carriage()
            name = ""
            idx = 0

            while header[idx] != ":":
                name += header[idx]
                idx += 1
            idx += 1
            while header[idx] == " ":
                idx += 1
            value = header[idx:]
            headers[name] = value

        return headers

    def extract_till_space(self):
        buffer = ""
        while self.current() != " ":
            buffer += self.current()
            self.cursor += 1

        self.cursor += 1
        return buffer

    def extract_till_carriage(self):
        buffer = ""

        while self.cursor + 4 <= self.length:
            if self.current() == '\r' \
                    and self.next() == '\n':
                return buffer

            buffer += self.current()
            self.cursor += 1

        return buffer

    def skip_carriage(self):
        match_count = 0

        while self.current() == "\r" and self.next() == "\n":
            self.cursor += 2
            match_count += 1

        return match_count
