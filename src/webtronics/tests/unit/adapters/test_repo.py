import os

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from webtronics.api.adapters.repo import (
    PostRepo,
    ReactionRepo,
    RepoError,
    UserRepo,
)
from webtronics.db.models import Post, Reaction, User


@pytest.fixture
def database_url():
    return os.getenv('WT_DATABASE_URL')


@pytest.fixture
def sessionmaker(database_url):
    engine = create_async_engine(database_url)
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.mark.asyncio
async def test_user_repo(sessionmaker):

    async with sessionmaker() as session:
        stmt = delete(Post)
        await session.execute(stmt)
        stmt = delete(User)
        await session.execute(stmt)
        await session.commit()

    user_repo = UserRepo(sessionmaker=sessionmaker)

    user = await user_repo.create('m@local', 'm', 'super_hashed_pass')
    assert user.email == 'm@local'
    assert user.username == 'm'
    assert user.hashed_password == 'super_hashed_pass'

    with pytest.raises(RepoError):
        user = await user_repo.create('m@local', 'm', 'super_hashed_pass')

    user = await user_repo.read_one('m@local')
    assert user.email == 'm@local'
    assert user.username == 'm'
    assert user.hashed_password == 'super_hashed_pass'

    with pytest.raises(RepoError):
        user = await user_repo.read_one('not_m@local')


@pytest.mark.asyncio
async def test_post_repo(sessionmaker):

    async with sessionmaker() as session:
        stmt = delete(Reaction)
        await session.execute(stmt)
        stmt = delete(Post)
        await session.execute(stmt)
        stmt = delete(User)
        await session.execute(stmt)
        await session.commit()

    user_repo = UserRepo(sessionmaker=sessionmaker)
    user = await user_repo.create('m@local', 'm', 'super_hashed_pass')
    another_user = await user_repo.create(
        'n@local', 'n', 'another_hashed_pass'
    )
    post_repo = PostRepo(sessionmaker=sessionmaker)

    new_post = await post_repo.create('title', 'text', user.id)
    assert new_post is not None
    assert new_post.title == 'title'
    assert new_post.text == 'text'
    assert new_post.author.id == user.id
    assert new_post.author.username == 'm'
    assert new_post.author.email == 'm@local'

    new_post = await post_repo.create('title', 'text', user.id)
    current_author_posts = await post_repo.read_many(author_id=user.id)
    current_all_posts = await post_repo.read_many()
    no_posts = await post_repo.read_many(author_id=another_user.id)

    assert len(current_author_posts) == len(current_all_posts)
    assert len(no_posts) == 0

    post_id = new_post.id
    found_post = await post_repo.read_one(post_id)
    assert found_post is not None
    assert found_post.title == 'title'
    assert found_post.text == 'text'

    patched_post = await post_repo.patch(post_id, title='new title')
    assert patched_post.title == 'new title'
    patched_post = await post_repo.patch(post_id, text='new text')
    assert patched_post.text == 'new text'

    await post_repo.delete(post_id)
    assert new_post.title == 'title'
    assert new_post.text == 'text'
    assert new_post.author.id == user.id
    assert new_post.author.username == 'm'
    assert new_post.author.email == 'm@local'

    with pytest.raises(RepoError):
        await post_repo.read_one(post_id=666)
    with pytest.raises(RepoError):
        await post_repo.patch(post_id=666, title='oh', text='no')
    with pytest.raises(RepoError):
        await post_repo.delete(post_id=666)


@pytest.mark.asyncio
async def test_reaction_repo(sessionmaker):

    async with sessionmaker() as session:
        stmt = delete(Reaction)
        await session.execute(stmt)
        stmt = delete(Post)
        await session.execute(stmt)
        stmt = delete(User)
        await session.execute(stmt)
        await session.commit()

    user_repo = UserRepo(sessionmaker=sessionmaker)
    post_repo = PostRepo(sessionmaker=sessionmaker)

    user1 = await user_repo.create('m@local', 'm', 'super_hashed_pass')
    user2 = await user_repo.create('n@local', 'n', 'another_hashed_pass')
    post = await post_repo.create('title', 'text', user1.id)

    reaction_repo = ReactionRepo(sessionmaker=sessionmaker)

    reactions = await reaction_repo.create(user2.id, post.id)
    assert len(reactions['likes']) == 1
    assert len(reactions['dislikes']) == 0
