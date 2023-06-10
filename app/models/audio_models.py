from sqlalchemy import Column, Integer, String, LargeBinary

from app.database.database import Base


class Audio(Base):
    """
    Defines the audio`s model
    """

    __tablename__ = "audios"
    audio_id = Column(String, primary_key=True, unique=True, index=True)
    user_id = Column(Integer, primary_key=True, index=True)  # Это foreign key
    audio_data = Column(LargeBinary)
