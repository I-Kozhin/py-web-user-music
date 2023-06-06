from sqlalchemy.ext.asyncio import create_async_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
import os

host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '5432')
user = os.getenv('DB_USER', 'user')
password = os.getenv('DB_PASSWORD', '123456789')
db = os.getenv('DB_NAME', 'postgresdb')
dbtype = os.getenv('DB_TYPE', 'postgresql')

SQLALCHEMY_DATABASE_URL = f"{dbtype}+asyncpg://{user}:{password}@{host}:{port}/{db}"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
