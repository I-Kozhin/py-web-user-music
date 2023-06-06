import logging
import sys
from typing import List, Type

from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

# from database.question import Question
# from dto.question_dto import QuestionDto
from app.models.user_models import User, UserDto

# Create a logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class CommitError(Exception):
    def __init__(self, message):
        super().__init__(message)
        # Terminate the program
        sys.exit(1)


class UserRepository:
    pass

    @staticmethod
    async def is_user_exists_by_name(user_name: str, session: AsyncSession) -> bool:
        query = select(User).filter(User.user_name == user_name).first()
        result = await session.execute(query)
        return result is not None

    @staticmethod
    async def add_user_to_database(new_user: User, session: AsyncSession) -> User:
        session.add(new_user)
        try:
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(f"An error occurred: {error}")
            raise CommitError("Commit failed. Program terminated.")
        return new_user


    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> UserDto:
        query = select(User).filter(User.user_id == user_id)
        result = await session.execute(query).first()
        result = UserDto.from_bd(result)
        return result
