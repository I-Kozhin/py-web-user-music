import os

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

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


def get_table_names(sync_conn):
    inspector = inspect(sync_conn)
    return inspector.get_table_names()


async def get_table_names_async():
    async with engine.begin() as conn:
        return await conn.run_sync(get_table_names)


async def init_models():
    table_names = await get_table_names_async()
    if db not in table_names:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
