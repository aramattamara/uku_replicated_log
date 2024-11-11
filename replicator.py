import logging
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Callable, Iterator

import requests
from requests import Response

TIMEOUT_S = 1.0
THREADS = 16

logger = logging.getLogger('replicator')


class Status(Enum):
    SUCCESS = 1
    TIMEOUT = 2
    FAILURE = 3
    ERROR = 4

    def __repr__(self):
        return self.name


class Replicator:
    def __init__(self, secondaries: list[str]):
        self.secondaries = secondaries
        self.pool = ThreadPoolExecutor(max_workers=THREADS)

    def replicate_message(self, message: str) -> list[Status]:
        results: Iterator[Status] = self.pool.map(
            self.send_message(message),
            self.secondaries,
            timeout=TIMEOUT_S + 1.0
        )
        return list(results)

    def send_message(self, message: str) -> Callable[[str], Status]:
        def send(secondary: str) -> Status:
            try:
                response: Response = requests.post(secondary, data=message, timeout=TIMEOUT_S)
            except requests.exceptions.ReadTimeout as e:
                logger.warning(f'Secondary {secondary} timed out for message {message}: {e}')
                return Status.TIMEOUT
            except IOError as e:
                logger.warning(f'Error sending {message} to {secondary}: {e}')
                return Status.ERROR

            if response.status_code == 200:
                logger.info(f"Replicated to {secondary}, response: {response.content}")
                return Status.SUCCESS
            else:
                logger.error(f"Failed to replicate to {secondary}: {response.status_code}")
                return Status.FAILURE

        return send
