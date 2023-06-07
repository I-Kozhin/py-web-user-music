from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_session_manager import get_session
from app.services.audio_services import AudioService

audio_router = APIRouter()

HOST = 'localhost'
PORT = 8000


@audio_router.post("/add-audio/", response_model=str)
async def add_audio(user_id: int, user_token: str, audio_wav, audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> str:
    with open('test_music.wav', 'rb') as f:  # for testing
        audio_wav = f.read()
        try:
            audio = await audio_service.add_audio_wav(user_id, user_token, audio_wav, session)
        except:
            raise
    return f'http://{HOST}:{PORT}/record?audio_id={audio.audio_id}&user_id={audio.user_id}'


@audio_router.get("/record", response_model=bytes, name="get_audio")
async def get_audio(audio_id: str, user_id: int, audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> bytes:
    try:
        audio = await audio_service.get_audio_mp3(audio_id, user_id, session)
    except:
        raise

    return Response(content=audio.audio_data, media_type='audio/wav',
                    headers={'Content-Disposition': 'attachment; filename=audio_you_wanted.wav'})
    # return Response(content=audio.audio_rec, media_type='audio/wav', filename=f'{audio_id}.wav')   # Здесь получаем
    # аудиозапись

# @audio_router.get("/get_download_link/")
# async def get_download_link(request: Request, record_id: str = Query(...), user_id: int = Query(...)) -> str:
#     url = request.url_for("get_audio", record_id=record_id, user_id=user_id)
#     return url
