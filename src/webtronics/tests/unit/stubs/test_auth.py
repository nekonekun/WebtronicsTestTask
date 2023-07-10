import pytest

from webtronics.api.stubs import AuthStub


@pytest.mark.asyncio
async def test_stub():
    auth_stub = AuthStub()
    with pytest.raises(NotImplementedError):
        await auth_stub.sign_up('m@local', 'm', 'raw_pass')

    with pytest.raises(NotImplementedError):
        await auth_stub.sign_in('m@local', 'raw_pass')

    assert auth_stub() == auth_stub
