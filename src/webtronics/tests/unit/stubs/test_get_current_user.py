import pytest

from webtronics.api.stubs import get_current_user_stub


@pytest.mark.asyncio
async def test_get_current_user():
    with pytest.raises(NotImplementedError):
        await get_current_user_stub()
