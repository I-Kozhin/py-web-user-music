from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_session_manager import get_session
from app.services.audio_services import AudioService
from app.models.audio_models import AudioDto

audio_router = APIRouter()


@audio_router.post("/add-audio/", response_model=str)
async def add_audio(user_id: int, user_token: str, audio_wav, audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> str:
    with open('test_music.wav', 'rb') as f:
        audio_wav = f.read()
        try:
            audio = await audio_service.add_audio_wav(user_id, user_token, audio_wav, session)
        except:
            raise

    return audio.audio_url


@audio_router.get("/record", response_model=str)
async def get_audio(audio_id: str, user_id: int, audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> str:
    try:
        audio = await audio_service.get_audio_mp3(audio_id, user_id, session)
    except:
        raise

    return audio.audio_url
