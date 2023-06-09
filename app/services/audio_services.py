from io import BytesIO

from fastapi import UploadFile
from pydub import AudioSegment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.audio_models import Audio
from app.repositories.audio_repository import AudioRepository
from app.services.token_generator import create_token


class AudioService:
    audio_repository: AudioRepository

    def __init__(self):
        self.audio_repository = AudioRepository()

    async def is_valid_id(self, user_id: int, session: AsyncSession) -> bool:
        return await self.audio_repository.validate_id(user_id, session)

    async def is_valid_token_to_id(self, user_id: int, user_token: str, session: AsyncSession) -> bool:
        return await self.audio_repository.validate_id_by_token(user_id, user_token, session)

    @staticmethod
    async def convert_from_wav_to_mp3(audio_wav: UploadFile) -> BytesIO:
        new_mp3_file = AudioSegment.from_wav(audio_wav.file)
        converted_audio = BytesIO()
        new_mp3_file.export(converted_audio, format='mp3')
        converted_audio.seek(0)
        return converted_audio

    # create audio
    async def add_audio_wav(self, user_id: int, user_token: str, audio_wav: UploadFile, session: AsyncSession) -> Audio:
        if await self.is_valid_token_to_id(user_id, user_token, session):
            audio_mp3 = await self.convert_from_wav_to_mp3(audio_wav)
            audio = await self.audio_repository.add_audio_to_database(
                Audio(audio_id=create_token(), user_id=user_id, user_token=user_token, audio_data=audio_mp3.read()),
                session) #  логику создания аудио отдать репозиторию, передавать туда только user_id, audio_data
        else:
            pass

        return audio

    async def get_audio(self, audio_id: str, user_id: int, session: AsyncSession) -> Audio:
        if await self.is_valid_id(user_id, session):  # Добавить проверку id записи
            result = await self.audio_repository.get_audio_by_id(audio_id, session)
        else:
            pass

        return result
