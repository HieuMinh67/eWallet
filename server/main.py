import time
from http.server import HTTPServer

from server.custom_server import Server
import logging

HOST = "localhost"
PORT = 8000


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info(f' {time.asctime()} Server Starts - {HOST}:{PORT}')
    http_server = HTTPServer((HOST, PORT), Server)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    http_server.server_close()
    logging.info(f'{time.asctime()} Server down')


if __name__ == "__main__":
    main()
