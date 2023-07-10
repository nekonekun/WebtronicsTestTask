import pytest

from webtronics.api.stubs import PosterStub


@pytest.mark.asyncio
async def test_stub():
    poster_stub = PosterStub()
    with pytest.raises(NotImplementedError):
        await poster_stub.create('title', 'text', 0)
    with pytest.raises(NotImplementedError):
        await poster_stub.read_one(0)
    with pytest.raises(NotImplementedError):
        await poster_stub.read_many()
    with pytest.raises(NotImplementedError):
        await poster_stub.patch(0)
    with pytest.raises(NotImplementedError):
        await poster_stub.delete(0)
    with pytest.raises(NotImplementedError):
        await poster_stub.react(0, 0)
    assert poster_stub() == poster_stub
