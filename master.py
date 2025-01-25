import logging
import time

from flask import Flask, jsonify, request

from message import Message
from replicator import Replicator

ADDR = '0.0.0.0'

logging.basicConfig(level='INFO')
logger = logging.getLogger('master')
app = Flask(__name__)

secondaries = [
    "http://secondary1:8000",
    "http://secondary2:8000",
]

total_nodes = 1 + len(secondaries)
logger.warning('Even number of total nodes')

replicator = Replicator(secondaries)

MASTER_LOG = []


@app.route('/', methods=['GET'])
def get():
    return jsonify(MASTER_LOG)


@app.route('/<message>', methods=['POST'])
def post(message: str):

    concern_str: str | None = request.args.get('concern')
    if concern_str is None:
        write_concern = len(secondaries)
    else:
        write_concern: int = int(concern_str)

    timestamp = time.time()

    full_message = Message(message, timestamp, write_concern)

    MASTER_LOG.append(full_message)

    logger.info(f"Added '{full_message}', current log {MASTER_LOG}, sending to replicas")

    quorum_reached: bool = replicator.replicate_message(full_message)

    if quorum_reached:
        print('Quorum reached')
    else:
        print('No quorum')

    return jsonify(f"Sent {full_message.content}: {str(quorum_reached)}")


def main(port: int, localhost: bool):
    if localhost:
        secondaries.clear()
        secondaries.extend([
            "http://localhost:3001",
            "http://localhost:3002",
        ])
    logger.info(f"Starting master on {ADDR} port {port}...")
    app.run(host=ADDR, port=port)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='bind to this port')
    parser.add_argument('--localhost', action='store_true', help='connect to the localhost when true')
    args = parser.parse_args()

    main(args.port, args.localhost)
