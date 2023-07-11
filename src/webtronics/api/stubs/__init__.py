"""Stubs collection"""
from typing import Annotated

from fastapi import Cookie, Header

from webtronics.api.stubs.auth import AuthStub
from webtronics.api.stubs.poster import PosterStub

__all__ = [
    'AuthStub',
    'PosterStub',
    'auth_stub',
    'poster_stub',
    'get_current_user_stub',
]


auth_stub = AuthStub()
poster_stub = PosterStub()


async def get_current_user_stub(
    auth_header: Annotated[str | None, Header(alias='Authentication')] = None,
    auth_cookie: Annotated[str | None, Cookie(alias='access')] = None,
):
    raise NotImplementedError
