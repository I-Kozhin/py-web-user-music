from fastapi import APIRouter, Depends, Response, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_session_manager import get_session
from app.services.audio_services import AudioService
from app.settings import HOST, PORT

audio_router = APIRouter()

# глобально сервис
@audio_router.post("/add-audio/")
async def add_audio(user_id: int, user_token: str, audio_wav: UploadFile = File(...),
                    audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> str:
    converted_audio = await audio_service.convert_from_wav_to_mp3(audio_wav)  # нужно вызвать сервис один раз
    try:
        audio = await audio_service.add_audio_wav(user_id, user_token, converted_audio, session)
    except:
        raise
    return f"http://{HOST}:{PORT}/record?audio_id={audio.audio_id}&user_id={audio.user_id}"


@audio_router.get("/record", response_model=bytes, name="get_audio")
async def get_audio(audio_id: str, user_id: int, audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> bytes:
    try:
        audio = await audio_service.get_audio(audio_id, user_id, session)
    except:
        raise

    return Response(content=audio.audio_data, media_type='audio/mpeg',
                    headers={'Content-Disposition': 'attachment; filename=audio_you_wanted.mp3'})

#  я передаю в get id_user, token_user, id_audio
