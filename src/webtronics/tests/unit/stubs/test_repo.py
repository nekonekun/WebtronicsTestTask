import pytest

from webtronics.api.stubs import PostRepoStub, ReactionRepoStub, UserRepoStub


@pytest.mark.asyncio
async def test_stub():
    user_repo_stub = UserRepoStub()
    post_repo_stub = PostRepoStub()
    reaction_repo_stub = ReactionRepoStub()
    with pytest.raises(NotImplementedError):
        await user_repo_stub.read_one('m@local')
    with pytest.raises(NotImplementedError):
        await user_repo_stub.create('m@local', 'm', 'raw')
    assert user_repo_stub() == user_repo_stub
    with pytest.raises(NotImplementedError):
        await post_repo_stub.read_many()
    with pytest.raises(NotImplementedError):
        await post_repo_stub.read_one(0)
    with pytest.raises(NotImplementedError):
        await post_repo_stub.create('title', 'text', 0)
    with pytest.raises(NotImplementedError):
        await post_repo_stub.patch(0)
    with pytest.raises(NotImplementedError):
        await post_repo_stub.delete(0)
    assert post_repo_stub() == post_repo_stub
    with pytest.raises(NotImplementedError):
        await reaction_repo_stub.create(0, 0)
    assert reaction_repo_stub() == reaction_repo_stub
