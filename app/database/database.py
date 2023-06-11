import os
from app.errors import logger, SomeReconnectableError
from time import sleep

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_TYPE

intervals = [1, 3, 7]

host = os.getenv('DB_HOST', DB_HOST)
port = os.getenv('DB_PORT', DB_PORT)
user = os.getenv('DB_USER', DB_USER)
password = os.getenv('DB_PASSWORD', DB_PASSWORD)
db = os.getenv('DB_NAME', DB_NAME)
dbtype = os.getenv('DB_TYPE', DB_TYPE)

SQLALCHEMY_DATABASE_URL = f"{dbtype}+asyncpg://{user}:{password}@{host}:{port}/{db}"

try:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    Base = declarative_base()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
except SQLAlchemyError as er:
    logger.error(f"An error occurred while setting up SQLAlchemy :: {er}")
    raise


def get_table_names(sync_conn):
    try:
        inspector = inspect(sync_conn)
        return inspector.get_table_names()
    except SQLAlchemyError as e:
        raise SomeReconnectableError(f'No connection, because {e}')


async def get_table_names_async():
    try:
        async with engine.begin() as conn:
            return await conn.run_sync(get_table_names)
    except SQLAlchemyError as e:
        raise SomeReconnectableError(f'No connection, because {e}')


async def init_models():
    for timeout in intervals:
        try:
            table_names = await get_table_names_async()
        except SomeReconnectableError as e:
            logger.warning(f'Failed to connect: {e}')
            sleep(timeout)
            continue
        else:
            if 'users' or 'audios' not in table_names:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
            break
    else:
        # if there was no break
        raise SomeReconnectableError(f'Failed to perform {init_models}')
