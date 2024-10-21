import requests
import logging

TIMEOUT_S = 1.0

logger = logging.getLogger('replicator')


class Replicator:
    def __init__(self, secondaries: list[str]):
        self.secondaries = secondaries

    def replicate_message(self, message: str):

        for secondary in self.secondaries:
            try:
                response = requests.post(secondary, data=message, timeout=TIMEOUT_S)
            except requests.exceptions.ReadTimeout as e:
                logger.warning(f'Secondary {secondary} timed out for message {message}')
                continue

            if response.status_code == 200:
                logger.info(f"Replicated to {secondary}, response: {response.content}")
            else:
                logger.error(f"Failed to replicate to {secondary}: {response.status_code}")
                return False

        return True
