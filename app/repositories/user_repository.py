import logging

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.user_models import User
from app.errors import CommitError
from app.services.token_generator import create_token

# Create a logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class UserRepository:

    async def add_user_to_database(self, user_name: str, session: AsyncSession) -> User:
        new_user = self.creating_user_object(user_name)
        session.add(new_user)
        try:
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(f"An error occurred while commit in User repository: {error}")
            raise CommitError("Commit failed. User database.")
        return new_user

    @staticmethod
    async def validate_id_by_token(user_id: int, user_token: str, session: AsyncSession) -> bool:
        query = select(User).filter(and_(User.user_id == user_id, User.user_token == user_token))
        result = await session.execute(query)
        user = result.scalar()
        return user is not None

    @staticmethod
    def creating_user_object(user_name: str) -> User:
        return User(user_name=user_name, user_token=create_token())
