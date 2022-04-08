import json
import logging
from http.server import BaseHTTPRequestHandler

from app.constants import CONTENT_TYPE_JSON
from router import Router


class Server(BaseHTTPRequestHandler):
    router = Router()

    def _get_content_type(self, content):
        if isinstance(content, str):
            return "text/plain"
        return CONTENT_TYPE_JSON

    def _build_response(self, status_code, content):
        content_type = self._get_content_type(content)
        self.send_response(status_code)
        if status_code == 200:
            self.send_header('Content-type', content_type)
        self.end_headers()
        if isinstance(content, (bytes, bytearray)):
            response = content
        elif isinstance(content, dict):
            response = bytes(json.dumps(content), 'UTF-8')
        else:
            response = bytes(content, 'UTF-8')
        self.wfile.write(response)

    def do_POST(self):
        logging.info("Handle POST request")
        content_length = int(self.headers['Content-Length'])

        request_body = self.rfile.read(content_length).decode('UTF-8')
        request_body = json.loads(request_body)

        status_code, response = self.router.execute(path=self.path, request_body=request_body, headers=self.headers)
        self._build_response(status_code=status_code, content=response)

    def do_GET(self):
        logging.info("Handle GET request")
        status_code, response = self.router.execute(path=self.path, request_body=None)
        self._build_response(status_code=status_code, content=response)
