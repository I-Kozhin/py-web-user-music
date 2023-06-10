class CommitError(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserNameError(Exception):
    def __init__(self, message):
        super().__init__(message)

#  Нужно возвращать соответствубщий http статус
