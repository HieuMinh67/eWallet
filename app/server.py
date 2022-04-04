import os

from http.server import BaseHTTPRequestHandler
from app.routes.main import routes
from app.response.jsonHandler import JsonHandler
from app.response.badRequestHandler import BadRequestHandler

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        print(">>>>>>>> self.path: ")
        print(self.path)
        print(">>>>>>>> request_extension: ")
        request_extension = split_path[1]
        print(request_extension)

        if self.path in routes:
            handler = JsonHandler()
            handler.jsonParse(routes[self.path])
        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })




    def handle_http(self, handler):
        status_code = handler.getStatus()
        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = {
                "status": 404,
                "message": "404 Not Found"
            }
        self.end_headers()

        return content.encode()

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)