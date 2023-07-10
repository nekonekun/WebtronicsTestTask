import pytest

from webtronics.api.exceptions import PosterError
from webtronics.api.helpers.poster import PosterHelper


@pytest.mark.asyncio
async def test_poster(
    sessionmaker, user_repo, post_repo, reaction_repo, cleanup
):
    # async with sessionmaker() as session:
    #     stmt = delete(Post)
    #     await session.execute(stmt)
    #     stmt = delete(User)
    #     await session.execute(stmt)
    #     await session.commit()

    poster = PosterHelper(post_repo, reaction_repo)
    user = await user_repo.create('a@mail', 'a', '123')
    another_user = await user_repo.create('b@mail', 'b', '123')

    new_post = await poster.create('title', 'text', user.id)
    assert new_post.title == 'title'
    assert new_post.text == 'text'
    assert isinstance(new_post.id, int)
    assert new_post.author.id == user.id

    another_post = await poster.create('title', 'text', user.id)
    assert another_post.title == 'title'
    assert another_post.text == 'text'
    assert isinstance(another_post.id, int)
    assert another_post.author.id == user.id

    patched_post = await poster.patch(new_post.id, title='new title')
    assert patched_post.title == 'new title'
    patched_post = await poster.patch(new_post.id, text='new text')
    assert patched_post.text == 'new text'
    new_post = patched_post

    with pytest.raises(PosterError):
        await poster.patch(999, text='new text')

    post = await poster.read_one(another_post.id)
    assert post.id == another_post.id
    assert post.title == another_post.title
    assert post.text == another_post.text
    assert post.author.id == another_post.author.id

    with pytest.raises(PosterError):
        await poster.read_one(999)

    posts = await poster.read_many()
    assert posts
    assert isinstance(posts[0].id, int)
    assert isinstance(posts[0].title, str)
    assert isinstance(posts[0].text, str)

    deleted_post = await poster.delete(new_post.id)
    assert deleted_post.id == new_post.id
    assert deleted_post.title == new_post.title
    assert deleted_post.text == new_post.text
    assert deleted_post.author.id == new_post.author.id

    with pytest.raises(PosterError):
        await poster.delete(new_post.id)

    reactions = await poster.react(another_post.id, another_user.id, True)
    assert len(reactions.likes) == 1
    assert len(reactions.dislikes) == 0

    reactions = await poster.react(another_post.id, another_user.id, True)
    assert len(reactions.likes) == 1
    assert len(reactions.dislikes) == 0

    reactions = await poster.react(another_post.id, another_user.id, False)
    assert len(reactions.likes) == 0
    assert len(reactions.dislikes) == 1

    with pytest.raises(PosterError):
        await poster.react(another_post.id, user.id, True)

    with pytest.raises(PosterError):
        await poster.react(999, user.id, True)

    await poster.delete(another_post.id)
    posts = await poster.read_many()
    assert posts == []

    # async with sessionmaker() as session:
    #     stmt = delete(Post)
    #     await session.execute(stmt)
    #     stmt = delete(User)
    #     await session.execute(stmt)
    #     await session.commit()
