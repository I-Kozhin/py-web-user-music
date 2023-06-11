from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.user import UserDto
from app.repositories.user import UserRepository
from app.errors import logger


class UserService:
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    async def create_user(self, user_name: str, session: AsyncSession) -> UserDto:
        try:
            if self.is_valid_name(user_name):
                user = await self.user_repository.add_user_to_database(user_name, session)
                return UserDto.create_from_bd(user)
        except Exception as e:
            logger.exception(f'Failed to perform {self.create_user} func at {UserService}: {e}')
            raise HTTPException(status_code=500,
                                detail=f'An unexpected error occurred while creating user.')

    @staticmethod
    def is_valid_name(user_name: str) -> bool:
        if (len(user_name)) > 0 and not (user_name.isspace()):
            return True
        else:
            raise HTTPException(status_code=400, detail=f'Username is incorrect.')
