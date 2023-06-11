from io import BytesIO

from fastapi import UploadFile, HTTPException
from pydub import AudioSegment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # type: ignore

from app.models.audio import Audio
from app.repositories.audio import AudioRepository
from app.repositories.user import UserRepository


class AudioService:
    audio_repository: AudioRepository
    user_repository: UserRepository

    def __init__(self):
        self.audio_repository = AudioRepository()
        self.user_repository = UserRepository()

    # create audio
    async def create_audio(self, user_id: int, user_token: str, audio_wav: UploadFile, session: AsyncSession) -> Audio:
        if await self.is_valid_token_to_id(user_id, user_token, session):
            audio_mp3 = await self.convert_from_wav_to_mp3(audio_wav)
            audio = await self.audio_repository.add_audio_to_database(user_id, audio_mp3, session)
        else:
            raise HTTPException(status_code=400,
                                detail=f'The current access token is invalid for the user with the ID: {user_id}')

        return audio

    async def get_audio(self, audio_id: str, user_id: int, session: AsyncSession) -> Audio:
        if await self.is_valid_user_id(user_id, session):
            if await self.is_valid_audio_id(audio_id, session):
                result = await self.audio_repository.get_audio_by_id(audio_id, session)
            else:
                raise HTTPException(status_code=400, detail=f'There is no such audio_id: {audio_id}')
        else:
            raise HTTPException(status_code=400, detail=f'There is no such user with ID: {user_id}')

        return result

    @staticmethod
    async def convert_from_wav_to_mp3(audio_wav: UploadFile) -> BytesIO:
        new_mp3_file = AudioSegment.from_wav(audio_wav.file)
        converted_audio = BytesIO()
        new_mp3_file.export(converted_audio, format='mp3')
        converted_audio.seek(0)
        return converted_audio

    async def is_valid_user_id(self, user_id: int, session: AsyncSession) -> bool:
        return await self.audio_repository.validate_user_id(user_id, session)

    async def is_valid_audio_id(self, audio_id: str, session: AsyncSession) -> bool:
        return await self.audio_repository.validate_audio_id(audio_id, session)

    async def is_valid_token_to_id(self, user_id: int, user_token: str, session: AsyncSession) -> bool:
        return await self.user_repository.validate_id_by_token(user_id, user_token, session)
