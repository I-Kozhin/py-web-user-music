import uuid
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audio_models import Audio
from app.repositories.audio_repository import AudioRepository


class UserNameError(Exception):
    def __init__(self, message):
        super().__init__(message)


def create_token() -> str:
    return str(uuid.uuid4())


class AudioService:
    audio_repository: AudioRepository

    def __init__(self):
        self.audio_repository = AudioRepository()

    async def is_valid_id(self, user_id: int, session: AsyncSession) -> bool:
        return await self.audio_repository.validate_id(user_id, session)

    async def is_valid_token_to_id(self, user_id: int, user_token: str, session: AsyncSession) -> bool:
        return await self.audio_repository.validate_id_by_token(user_id, user_token, session)

    async def add_audio_wav(self, user_id: int, user_token: str, audio_wav, session: AsyncSession) -> Audio:
        if await self.is_valid_token_to_id(user_id, user_token, session):
            result = await self.audio_repository.add_audio_to_database(
                Audio(audio_id=create_token(), user_id=user_id, user_token=user_token, audio_data=audio_wav), session)
        else:
            pass

        return result

    async def get_audio_mp3(self, audio_id: str, user_id: int, session: AsyncSession) -> Audio:
        if await self.is_valid_id(user_id, session): # Добавить проверку id записи
            result = await self.audio_repository.get_audio_by_id(audio_id, session)
        else:
            pass

        return result

    # async def create_user(self, user_name: str, session: AsyncSession) -> UserDto:
    #     if self.is_valid_name(user_name):
    #         new_user_bd = User(user_name=user_name, user_token=create_token())
    #         result = await self.user_repository.add_user_to_database(new_user_bd, session)
    #         result = UserDto.from_bd(result)
    #         return result
    #     else:
    #         raise UserNameError("Username is incorrect.")
