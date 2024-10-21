import logging
from flask import Flask, request, jsonify
from replicator import Replicator

ADDR = '0.0.0.0'

logging.basicConfig(level='INFO')
logger = logging.getLogger('master')
app = Flask(__name__)


secondaries = [
     "http://secondary1:8000",
     "http://secondary2:8000",
]

replicator = Replicator(secondaries)

MASTER_LOG = []
@app.route('/', methods=['GET'])
def get():
    return jsonify(MASTER_LOG)


@app.route('/<message>', methods=['POST'])
def post(message: str):
    MASTER_LOG.append(message)

    logger.info(f"Added '{message}', current log {MASTER_LOG}, sending to replicas")

    replicator.replicate_message(message)

    return jsonify(f"Added {message}")


def main(port: int):
    logger.info(f"Starting Flask server on {ADDR} port {port}...")
    app.run(host=ADDR, port=port)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='bind to this port')
    args = parser.parse_args()

    main(args.port)
