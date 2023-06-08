import uuid

from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from app.database.database import Base


class UserDto(BaseModel):
    user_id: Optional[int]
    user_name: Optional[str]
    user_token: Optional[str]

    @classmethod
    def from_bd(cls, db_row: 'User') -> 'UserDto':
        return cls(
            user_id=db_row.user_id,
            user_name=db_row.user_name,
            user_token=db_row.user_token

        )

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_token": self.user_token
        }


class User(Base):
    """
    Defines the user`s model
    """

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    user_name = Column(String, index=True)
    user_token = Column(String, unique=True)


    @classmethod
    def from_dto(cls, dto: UserDto) -> 'User':
        return cls(
            user_name=dto.user_name,
            user_token=str(uuid.uuid4())
        )
