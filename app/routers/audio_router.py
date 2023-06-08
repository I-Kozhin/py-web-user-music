from fastapi import APIRouter, Depends, Response, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from pydub import AudioSegment
from io import BytesIO

from fastapi.responses import StreamingResponse
from app.database.database_session_manager import get_session
from app.services.audio_services import AudioService

audio_router = APIRouter()

HOST = 'localhost'
PORT = 8000


@audio_router.post("/add-audio/")
async def add_audio(user_id: int, user_token: str, audio_wav: UploadFile = File(...),
                    audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> str:
    new_mp3_file = AudioSegment.from_wav(audio_wav.file)
    converted_audio = BytesIO()
    new_mp3_file.export(converted_audio, format='mp3')
    converted_audio.seek(0)  # Reset the file pointer to the beginning

    # return StreamingResponse(converted_audio, media_type='audio/mpeg')
    try:
        audio = await audio_service.add_audio_wav(user_id, user_token, converted_audio, session)
    except:
        raise
    return f"http://{HOST}:{PORT}/record?audio_id={audio.audio_id}&user_id={audio.user_id}"


@audio_router.get("/record", response_model=bytes, name="get_audio")
async def get_audio(audio_id: str, user_id: int, audio_service: AudioService = Depends(AudioService),
                    session: AsyncSession = Depends(get_session)) -> bytes:
    try:
        audio = await audio_service.get_audio_mp3(audio_id, user_id, session)
    except:
        raise

    return Response(content=audio.audio_data, media_type='audio/mpeg',
                    headers={'Content-Disposition': 'attachment; filename=audio_you_wanted.mp3'})
