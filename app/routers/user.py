from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_session_manager import get_session
from app.models.user import UserDto
from app.services.user import UserService

user_router = APIRouter()
user_service = UserService()


@user_router.post("/create-user/", response_model=dict)
async def create_user(user_name: str, session: AsyncSession = Depends(get_session)) -> UserDto:
    try:
        user = await user_service.create_user(user_name, session)
    except:
        raise

    return user
