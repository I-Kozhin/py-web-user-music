from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, LargeBinary
from app.database.database import Base
import base64

# class AudioDto(BaseModel):
#     audio_id: Optional[str]
#     user_id: Optional[int]
#     user_token: Optional[str]
#     audio_rec: Optional[bytes]
#
#     # @property
#     # def audio_url(self):
#     #     return self.audio_url
#
#     @classmethod
#     def from_bd(cls, db_row: 'Audio') -> 'AudioDto':
#         return cls(
#             audio_id=db_row.audio_id,
#             user_id=db_row.user_id,
#             user_token=db_row.user_token,
#             audio_rec=db_row.audio_data
#         )


class Audio(Base):
    """
    Defines the audio`s model
    """

    __tablename__ = "audios"
    audio_id = Column(String, primary_key=True, unique=True, index=True, )
    user_id = Column(Integer, primary_key=True, index=True)
    user_token = Column(String)
    audio_data = Column(LargeBinary)
