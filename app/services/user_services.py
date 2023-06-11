from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.database.database_session_manager import get_session
from app.models.user import UserDto, User
from app.repositories.user import UserRepository
from app.services.token_generator import create_token
from app.errors import UserNameError


class UserService:
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    async def create_user(self, user_name: str, session: AsyncSession) -> UserDto:
        if self.is_valid_name(user_name):
            user = await self.user_repository.add_user_to_database(user_name, session)
            return UserDto.create_from_bd(user)
        else:
            raise UserNameError("Username is incorrect.")

    @staticmethod
    def is_valid_name(user_name: str) -> bool:
        return (len(user_name)) > 0 and not (user_name.isspace())
