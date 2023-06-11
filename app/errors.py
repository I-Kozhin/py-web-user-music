import logging


class CommitError(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserNameError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SomeReconnectableError(Exception):
    def __init__(self, message):
        super().__init__(message)


#  Нужно возвращать соответствубщий http статус

# except QuestionServiceError as error:
#         raise HTTPException(status_code=400, detail=str(error))

# Create a logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
