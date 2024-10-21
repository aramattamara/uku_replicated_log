import sys
import logging
from http import server
from http.server import ThreadingHTTPServer

ADDR = '0.0.0.0'
SECONDARY_LOG = []
logger = logging.getLogger('secondary')

class MyHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        response = str(SECONDARY_LOG)

        self.wfile.write(f"{response}\n".encode())

    def do_POST(self):
        #message = self.path
        message = self.rfile.read(9999999)
        SECONDARY_LOG.append(message)


        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        print(f"Added {self.path}, current {SECONDARY_LOG}")
        self.wfile.write(f"Added {self.path}\n".encode())


def main(port: int):
    with ThreadingHTTPServer((ADDR, port), MyHandler) as httpd:

        print(f"Serving HTTP on {ADDR} port {port} ")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='bind to this port')
    args = parser.parse_args()

    main(args.port)


