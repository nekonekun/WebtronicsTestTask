import time
from datetime import timedelta

import pytest

from webtronics.api.helpers.jwt import JWTHelper, JWTHelperError


@pytest.fixture
def jwt_helper():
    return JWTHelper(secret_key='1', token_lifetime=timedelta(seconds=2))


def test_token_creation_from_username(jwt_helper):
    token = jwt_helper.create_token('username')
    sub = jwt_helper.extract_sub(token)
    assert sub == 'username'


def test_token_creation_from_dict(jwt_helper):
    token = jwt_helper.create_token(
        {'sub': 'username', 'extra_field': 'extra_value'}
    )
    sub = jwt_helper.extract_sub(token)
    assert sub == 'username'


def test_token_invalid_data(jwt_helper):
    with pytest.raises(JWTHelperError):
        jwt_helper.create_token('')
    with pytest.raises(JWTHelperError):
        jwt_helper.create_token({'incorrect_field': 'incorrect_value'})
    with pytest.raises(JWTHelperError):
        jwt_helper.create_token(
            'username', token_lifetime=timedelta(seconds=-5)
        )
    jwt_helper.algorithm = 'INVALID_ALGORITHM'
    with pytest.raises(JWTHelperError):
        jwt_helper.create_token('username')


def test_token_lifetime(jwt_helper):
    token = jwt_helper.create_token(
        {'sub': 'username', 'extra_field': 'extra_value'}
    )
    time.sleep(3)
    with pytest.raises(JWTHelperError):
        jwt_helper.extract_sub(token)
