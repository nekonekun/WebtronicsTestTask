import os
import pytest
from passlib.context import CryptContext
from webtronics.db.models import Post, User
from sqlalchemy import delete


from webtronics.api.helpers.auth import AuthError, AuthHelper


@pytest.mark.asyncio
async def test_auth(sessionmaker, user_repo, jwt_helper, cleanup):
    # async with sessionmaker() as session:
    #     stmt = delete(Post)
    #     await session.execute(stmt)
    #     stmt = delete(User)
    #     await session.execute(stmt)
    #     await session.commit()

    auth_helper = AuthHelper(
        user_repo,
        CryptContext(schemes=['bcrypt'], deprecated='auto'),
        jwt_helper,
    )
    new_user = await auth_helper.sign_up('m@local', 'm', 'pass')
    assert new_user.email == 'm@local'
    assert new_user.username == 'm'

    with pytest.raises(AuthError):
        new_user = await auth_helper.sign_up('m@local', 'm', 'pass')

    await auth_helper.sign_in('m@local', 'pass')

    with pytest.raises(AuthError):
        await auth_helper.sign_in('m@local', 'fake')

    with pytest.raises(AuthError):
        await auth_helper.sign_in('fake@local', 'fake')

    # async with sessionmaker() as session:
    #     stmt = delete(Post)
    #     await session.execute(stmt)
    #     stmt = delete(User)
    #     await session.execute(stmt)
    #     await session.commit()
