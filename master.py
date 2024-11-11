import logging
from flask import Flask, jsonify
from replicator import Replicator, Status

ADDR = '0.0.0.0'

logging.basicConfig(level='INFO')
logger = logging.getLogger('master')
app = Flask(__name__)


secondaries = [
     "http://secondary1:8000",
     "http://secondary2:8000",
]
#DEBUG
# secondaries = [
#     "http://localhost:3001",
#     "http://localhost:3002",
# ]

total_nodes = 1 + len(secondaries)
logger.warning('Even number of total nodes')

replicator = Replicator(secondaries)

MASTER_LOG = []


@app.route('/', methods=['GET'])
def get():
    return jsonify(MASTER_LOG)


@app.route('/<message>', methods=['POST'])
def post(message: str):
    MASTER_LOG.append(message)

    logger.info(f"Added '{message}', current log {MASTER_LOG}, sending to replicas")

    results: list[Status] = replicator.replicate_message(message)

    # 1 for master + replicas
    total_successes = 1 + results.count(Status.SUCCESS)

    if total_successes > total_nodes // 2:
        print('Quorum reached')
    else:
        print('No quorum')

    return jsonify(f"Sent {message}: {str(results)}")


def main(port: int):
    logger.info(f"Starting master on {ADDR} port {port}...")
    app.run(host=ADDR, port=port)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='bind to this port')
    args = parser.parse_args()

    main(args.port)
