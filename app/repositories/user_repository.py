import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.user_models import User
from app.errors import CommitError

# Create a logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class UserRepository:

    @staticmethod
    async def add_user_to_database(new_user: User, session: AsyncSession) -> User:
        session.add(new_user)
        try:
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(f"An error occurred: {error}")
            raise CommitError("Commit failed. Program terminated.")
        return new_user
