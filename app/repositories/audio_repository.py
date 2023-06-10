import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.errors import CommitError
from app.models.audio_models import Audio
from app.models.user_models import User

# Create a logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class AudioRepository:

    @staticmethod
    async def add_audio_to_database(new_audio: Audio, session: AsyncSession) -> Audio:
        session.add(new_audio)
        try:
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(f"An error occurred: {error}")  # An error  while commit
            raise CommitError("Commit failed.")
        return new_audio

    @staticmethod
    async def get_audio_by_id(audio_id: str, session: AsyncSession) -> Audio:
        query = select(Audio).filter(Audio.audio_id == audio_id)
        result = await session.execute(query)
        audio = result.scalar()
        return audio

    @staticmethod
    async def validate_id(user_id: int, session: AsyncSession) -> bool:
        query = select(Audio).filter(Audio.user_id == user_id) # здесь только audio_id
        result = await session.execute(query)  # result.scalar()
        return result is not None
