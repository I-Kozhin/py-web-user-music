from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_session_manager import get_session
from app.services.user_services import UserService

user_router = APIRouter()
user_service = UserService()


# сделать user_service глобальным, чтобы я один раз объявил его

@user_router.post("/create-user/", response_model=dict)
async def create_user(user_name: str, session: AsyncSession = Depends(get_session)) -> dict:
    try:
        user = await user_service.create_user(user_name, session)
    except:
        raise

    return user  # вернуть всю dto - убрать лишние поля
