import logging


class CommitError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SomeReconnectableError(Exception):
    def __init__(self, message):
        super().__init__(message)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
