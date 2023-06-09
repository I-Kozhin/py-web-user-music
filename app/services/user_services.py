from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.user_models import UserDto, User
from app.repositories.user_repository import UserRepository
from app.services.token_generator import create_token
from app.errors import UserNameError


class UserService:
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    async def create_user(self, user_name: str) -> UserDto:
        if self.is_valid_name(user_name):
            user = await self.user_repository.add_user_to_database(user_name)
            return UserDto.create_from_bd(user)
        else:
            raise UserNameError("Username is incorrect.")

    @staticmethod
    def is_valid_name(user_name: str) -> bool:
        return (len(user_name)) > 0 and not (user_name.isspace())
