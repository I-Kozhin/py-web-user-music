from fastapi import APIRouter, Depends, Response, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_session_manager import get_session
from app.services.audio_services import AudioService
from app.settings import HOST_OUT, PORT

audio_router = APIRouter()
audio_service = AudioService()


@audio_router.post("/add-audio/")
async def add_audio(user_id: int, user_token: str, audio_wav: UploadFile = File(...),
                    session: AsyncSession = Depends(get_session)) -> str:
    try:
        audio = await audio_service.create_audio(user_id, user_token, audio_wav, session)
    except:
        raise
    return f"http://{HOST_OUT}:{PORT}/record?audio_id={audio.audio_id}&user_id={audio.user_id}"


@audio_router.get("/record", response_model=bytes, name="get_audio")
async def get_audio(audio_id: str, user_id: int, session: AsyncSession = Depends(get_session)) -> bytes:
    try:
        audio = await audio_service.get_audio(audio_id, user_id, session)
    except:
        raise

    return Response(content=audio.audio_data, media_type='audio/mpeg',
                    headers={'Content-Disposition': 'attachment; filename=audio_you_wanted.mp3'})

#  я передаю в get id_user, token_user, id_audio
