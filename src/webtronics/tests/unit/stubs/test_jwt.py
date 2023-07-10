import pytest

from webtronics.api.stubs import JWTStub


def test_stub():
    jwt_stub = JWTStub()
    with pytest.raises(NotImplementedError):
        jwt_stub.create_token('str')
    with pytest.raises(NotImplementedError):
        jwt_stub.extract_sub('str')
    assert jwt_stub() == jwt_stub
