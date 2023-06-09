from uuid import uuid4 as generator


def create_token() -> str:
    return str(generator())
