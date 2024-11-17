import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from enum import Enum

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

    def replicate_message(self, full_message: dict[str, str | float]) -> bool:

        ff: list[Future[Status]] = []

        for secondary in self.secondaries:
            # self.send_message(full_message, secondary)

            f: Future[Status] = self.pool.submit(
                self.send_message,
                full_message,
                secondary
            )
            ff.append(f)

        successful = 1  # Master itself counts as 1 ACK

        if full_message["concern"] == 1:
            return True

        f: Future[Status]
        for f in as_completed(ff):
            result = f.result(timeout=TIMEOUT_S + 1.0)

            if result == Status.SUCCESS:
                successful += 1

            if successful >= full_message["concern"]:
                return True
        return False


    def send_message(self, full_message: dict[str, str | float], secondary: str) -> Status:
        try:
            response: Response = requests.post(secondary, data=full_message, timeout=TIMEOUT_S)
        except requests.exceptions.ReadTimeout as e:
            logger.warning(f'Secondary {secondary} timed out for message {full_message}: {e}')
            return Status.TIMEOUT
        except IOError as e:
            logger.warning(f'Error sending {full_message} to {secondary}: {e}')
            return Status.ERROR

        if response.status_code == 200:
            logger.info(f"Replicated to {secondary}, response: {response.content}")
            return Status.SUCCESS
        else:
            logger.error(f"Failed to replicate to {secondary}: {response.status_code}")
            return Status.FAILURE
