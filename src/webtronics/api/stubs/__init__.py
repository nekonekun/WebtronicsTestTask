"""Stubs collection"""
from typing import Annotated

from fastapi import Cookie, Header

from webtronics.api.stubs.auth import AuthStub
from webtronics.api.stubs.jwt import JWTStub
from webtronics.api.stubs.poster import PosterStub
from webtronics.api.stubs.repo import (
    PostRepoStub,
    ReactionRepoStub,
    UserRepoStub,
)
from webtronics.api.stubs.verifier import EmailVerifierStub

__all__ = [
    'UserRepoStub',
    'PostRepoStub',
    'ReactionRepoStub',
    'AuthStub',
    'JWTStub',
    'PosterStub',
    'EmailVerifierStub',
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
