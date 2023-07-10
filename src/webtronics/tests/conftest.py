import asyncio
import os
from datetime import timedelta

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from webtronics.api.adapters.repo import PostRepo, ReactionRepo, UserRepo
from webtronics.api.helpers.jwt import JWTHelper
from webtronics.db.models import Post, User


@pytest.fixture(scope='session')
def database_url():
    return os.getenv('WT_DATABASE_URL')


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def sessionmaker(event_loop, database_url):
    engine = create_async_engine(database_url)
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope='session')
def user_repo(sessionmaker, event_loop):
    return UserRepo(sessionmaker)


@pytest.fixture(scope='session')
def post_repo(sessionmaker, event_loop):
    return PostRepo(sessionmaker)


@pytest.fixture(scope='session')
def reaction_repo(sessionmaker, event_loop):
    return ReactionRepo(sessionmaker)


@pytest.fixture(scope='session')
def jwt_helper(event_loop):
    return JWTHelper(secret_key='1', token_lifetime=timedelta(days=1))


@pytest.fixture
async def cleanup(sessionmaker):
    async with sessionmaker() as session:
        stmt = delete(Post)
        await session.execute(stmt)
        stmt = delete(User)
        await session.execute(stmt)
        await session.commit()
