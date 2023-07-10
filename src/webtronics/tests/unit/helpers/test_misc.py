import pytest
from fastapi import HTTPException
from webtronics.api.helpers.misc import get_current_user_factory
from webtronics.db.models import Post, User
from sqlalchemy import delete


@pytest.mark.asyncio
async def test_get_current_user(sessionmaker, user_repo, jwt_helper, cleanup):
    # async with sessionmaker() as session:
    #     stmt = delete(Post)
    #     await session.execute(stmt)
    #     stmt = delete(User)
    #     await session.execute(stmt)
    #     await session.commit()

    await user_repo.create('e@mail', 'e', 'pass')
    get_current_user = get_current_user_factory(user_repo, jwt_helper)
    token = jwt_helper.create_token('e@mail')
    with pytest.raises(HTTPException):
        await get_current_user()
    current_user = await get_current_user(auth_header=token)
    assert current_user.email == 'e@mail'
    current_user = await get_current_user(auth_cookie=token)
    assert current_user.email == 'e@mail'
    with pytest.raises(HTTPException):
        await get_current_user('f@mail')

    # async with sessionmaker() as session:
    #     stmt = delete(Post)
    #     await session.execute(stmt)
    #     stmt = delete(User)
    #     await session.execute(stmt)
    #     await session.commit()
