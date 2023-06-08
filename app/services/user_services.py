import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.user_models import UserDto, User
from app.repositories.user_repository import UserRepository


class UserNameError(Exception):
    def __init__(self, message):
        super().__init__(message)


def create_token() -> str:
    return str(uuid.uuid4())


class UserService:
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    @staticmethod
    def is_valid_name(user_name: str) -> bool:
        return (len(user_name)) > 0 and not (user_name.isspace())

    async def create_user(self, user_name: str, session: AsyncSession) -> UserDto:
        if self.is_valid_name(user_name):
            new_user_bd = User(user_name=user_name, user_token=create_token())
            result = await self.user_repository.add_user_to_database(new_user_bd, session)
            result = UserDto.from_bd(result)
            return result
        else:
            raise UserNameError("Username is incorrect.")
