import sys
import logging

import requests
from http import server
from http.server import ThreadingHTTPServer

from replicator import Replicator

ADDR = '0.0.0.0'

MASTER_LOG = []

# Configure logging
logger = logging.getLogger('master')


requests.get('secondary2:8000')

secondaries33 = [
    "http://secondary1:3001",
    "http://secondary2:3002",
]

replicator = Replicator(secondaries33)


class MyHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        response = str(MASTER_LOG)
        self.wfile.write(f"{response}\n".encode())

    def do_POST(self):
        message = self.path

        MASTER_LOG.append(message)

        print(f"Added {self.path}, current log {MASTER_LOG}")

        self.wfile.write(f"Added {self.path}\n".encode())

        replicator.replicate_message(message)


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











@app.route('/log', methods=['POST'])
def append_log():
    message = request.json.get('message')
    if not message:
        return "No message", 400

    master_log.append(message)


    # for secondary in secondaries:
    #     try:
    #         res = request.post(f"{secondary}/log", json={'message':message})
    #         if response.status_code != 200:
    #             return f"Failed ti replicate to {secondary}", 500




if __name__ == '__main__':
    logger.info("Starting Master server...")
    app.run(port=5000)
