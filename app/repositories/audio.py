from fastapi import HTTPException

from app.errors import logger

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from io import BytesIO
from app.errors import CommitError
from app.models.audio import Audio
from app.services.token_generator import create_token


class AudioRepository:

    async def add_audio_to_database(self, user_id: int, audio_data: BytesIO, session: AsyncSession) -> Audio:
        new_audio = self.create_audio_object(user_id, audio_data)
        session.add(new_audio)
        try:
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(f"An error occurred while committing in the Audio repository:: {error}")
            raise CommitError("Commit failed. Audios table.")
        return new_audio

    @staticmethod
    async def get_audio_by_id(audio_id: str, session: AsyncSession) -> Audio:
        query = select(Audio).filter(Audio.audio_id == audio_id)
        result = await session.execute(query)
        audio = result.scalar()
        return audio

    @staticmethod
    async def validate_user_id(user_id: int, session: AsyncSession) -> bool:
        query = select(Audio).filter(Audio.user_id == user_id)
        result = await session.execute(query)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=400, detail=f'There is no such user with ID: {user_id}')

    @staticmethod
    async def validate_audio_id(audio_id: str, session: AsyncSession) -> bool:
        query = select(Audio).filter(Audio.audio_id == audio_id)
        result = await session.execute(query)
        result = result.scalar()
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=400, detail=f'There is no such audio with ID: {audio_id}')

    @staticmethod
    def create_audio_object(user_id: int, audio_data: BytesIO) -> Audio:
        return Audio(audio_id=create_token(), user_id=user_id, audio_data=audio_data.read())
