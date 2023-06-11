from fastapi import APIRouter, Depends, Response, File, UploadFile, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import urlparse

from app.database.database_session_manager import get_session
from app.services.audio import AudioService
from app.settings import PORT
from app.errors import logger

audio_router = APIRouter()
audio_service = AudioService()


@audio_router.post("/add-audio/")
async def add_audio(user_id: int, user_token: str, request: Request, audio_wav: UploadFile = File(...),
                    session: AsyncSession = Depends(get_session)) -> str:
    try:
        audio = await audio_service.create_audio(user_id, user_token, audio_wav, session)
        parsed_url = urlparse(f'{request.url}')
        ip_address = parsed_url.hostname
        return f"http://{ip_address}:{PORT}/record?audio_id={audio.audio_id}&user_id={audio.user_id}"
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f'Failed to perform {add_audio} func: {e}')
        raise HTTPException(status_code=500,
                            detail=f'An unexpected error occurred while doing post-request.')


@audio_router.get("/record", response_model=bytes, name="get_audio")
async def get_audio(audio_id: str, user_id: int, session: AsyncSession = Depends(get_session)) -> Response:
    try:
        audio = await audio_service.get_audio(audio_id, user_id, session)
        return Response(content=audio.audio_data, media_type='audio/mpeg',
                        headers={'Content-Disposition': 'attachment; filename=audio_you_wanted.mp3'})
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f'Failed to perform {get_audio} func: {e}')
        raise HTTPException(status_code=500,
                            detail=f'An unexpected error occurred while doing get-request.')
