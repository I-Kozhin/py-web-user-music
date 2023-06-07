from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_session_manager import get_session
# from service.question_service import QuestionService, QuestionServiceError
from app.services.user_services import UserService
from app.models.user_models import UserDto

user_router = APIRouter()


@user_router.post("/create-user/", response_model=dict)
async def create_user(user_name: str, user_service: UserService = Depends(UserService),
                      session: AsyncSession = Depends(get_session)) -> dict:
    try:
        user = await user_service.create_user(user_name, session)
    except:
        raise

    return user.to_dict()
