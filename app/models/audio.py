from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Audio(Base):
    """
    Defines the audio`s model
    """
    __tablename__ = "audios"

    audio_id = Column(String, primary_key=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    audio_data = Column(LargeBinary)

    user = relationship("User", back_populates="audios")
