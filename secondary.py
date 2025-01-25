import logging
import time

from flask import Flask, request, jsonify

ADDR = '0.0.0.0'

logging.basicConfig(level='INFO')
logger = logging.getLogger('secondary')
app = Flask(__name__)

SECONDARY_LOG = []


@app.route('/', methods=['GET'])
def get():
    return jsonify(SECONDARY_LOG)


@app.route('/', methods=['POST'])
def post():
    message = request.data.decode('utf-8')
    logger.info(f"Received {message}")

    time.sleep(0.994)  # DEBUG

    SECONDARY_LOG.append(message)

    logger.info(f"Current {SECONDARY_LOG}")

    return jsonify(f"Added {message}")


def main(port: int):
    logger.info(f"Starting secondary on {ADDR} port {port}...")
    app.run(host=ADDR, port=port)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='bind to this port')
    args = parser.parse_args()

    main(args.port)


