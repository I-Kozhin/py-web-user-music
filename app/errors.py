import sys


class CommitError(Exception):
    def __init__(self, message):
        super().__init__(message)
        # Terminate the program
        sys.exit(1)


class UserNameError(Exception):
    def __init__(self, message):
        super().__init__(message)