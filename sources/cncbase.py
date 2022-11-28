from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import cgi
import json
import traceback


class CNCBase(BaseHTTPRequestHandler):

    def do_generic(self, method:str, body:dict):
        try:
            path, params = self.parse_url(self.path)
            function_name = self.get_function_name(path)
            self.log_message(f"function : {function_name}, path : {path}, params : {params}")

            func = getattr(self, f"{method}_{function_name}")
            response = func(path, params, body)

            self.end_of_transaction(200, response)
        except Exception as e:
            self.log_error(traceback.format_exc())
            self.end_of_transaction(500, {})



    def end_of_transaction(self, code:int, response:dict):
        if not isinstance(response, dict):
                response = {}

        json_data = json.dumps(response)
        response_body = bytes(json_data, "utf8")
        self.send_response(code)
        self.end_headers()
        self.wfile.write(response_body)



    def do_GET(self):
        return self.do_generic("get", {})



    def do_POST(self):
        content_type = self.headers.get('content-type')
        ctype, _ = cgi.parse_header(content_type)
        body = {}
        if ctype == 'application/json':
            length = int(self.headers.get('content-length'))
            body = json.loads(self.rfile.read(length))

        else:
            raise Exception("bad content-type")

        return self.do_generic("post", body)



    def parse_url(self, url):
        fields = urlparse(url)

        params = dict()

        if fields.query == "":
            return fields.path, params

        for key_value in fields.query.split("&"):
            try:
                key, value = key_value.split("=")
                params[key] = value
            except ValueError as e:
                self.log_error(f"'{key_value}' is not splitable")
                self.log_error(traceback.format_exc())

        return fields.path, params



    def get_function_name(self, path:str):
        path = path[1:] # remove /
        return path.split("/")[0]
