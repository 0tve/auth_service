from collections import abc

import asyncpg
import fastapi
import sqlalchemy
from fastapi import status
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.entities import db, models

async_default_engine = sa_asyncio.create_async_engine(
    db.db_default_credentials.url)
async_default_sessionmaker = sa_asyncio.async_sessionmaker(
    async_default_engine)

async_engine = sa_asyncio.create_async_engine(db.db_credentials.url)
async_sessionmaker = sa_asyncio.async_sessionmaker(async_engine)


async def is_db_exists(sessionmaker: sa_asyncio.async_sessionmaker) -> bool:
    try:
        async with sessionmaker() as session:
            session: sa_asyncio.AsyncSession
            await session.execute(sqlalchemy.text('SELECT 1'))
            return True
    except (asyncpg.InvalidCatalogNameError, asyncpg.ConnectionDoesNotExistError):
        return False


async def ensure_db_exists() -> None:
    default_db_exists = await is_db_exists(async_default_sessionmaker)
    db_exists = await is_db_exists(async_sessionmaker)
    if not default_db_exists and not db_exists:
        raise fastapi.HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                                    detail='Не создана ни одна из указанных баз данных, продолжение работы невозможно')
    if db_exists:
        return
    async with async_default_engine.connect() as conn:
        conn: sa_asyncio.AsyncConnection = await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(sqlalchemy.text(f'CREATE DATABASE {db.db_credentials.name}'))


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def get_session() -> abc.AsyncIterator[sa_asyncio.AsyncSession]:
    async with async_sessionmaker() as session:
        yield session
