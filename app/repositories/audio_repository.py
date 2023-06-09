import logging
import sys

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.audio_models import Audio
from app.models.user_models import User
from app.errors import CommitError

# Create a logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class AudioRepository:

    @staticmethod
    async def validate_id_by_token(user_id: int, user_token: str, session: AsyncSession) -> bool:
        query = select(User).filter(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalar()  # .scalar() will return the User instance directly
        if user is None:
            return False
        return user.user_token == user_token

    @staticmethod
    async def validate_id(user_id: int, session: AsyncSession) -> bool:
        query = select(Audio).filter(Audio.user_id == user_id)
        result = await session.execute(query)
        return result is not None

    @staticmethod
    async def add_audio_to_database(new_audio: Audio, session: AsyncSession) -> Audio:
        session.add(new_audio)
        try:
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(f"An error occurred: {error}")
            raise CommitError("Commit failed. Program terminated.")
        return new_audio

    @staticmethod
    async def get_audio_by_id(audio_id: str, session: AsyncSession) -> Audio:
        query = select(Audio).filter(Audio.audio_id == audio_id)
        result = await session.execute(query)
        audio = result.scalar()  # .scalar() will return the User instance directly
        return audio
