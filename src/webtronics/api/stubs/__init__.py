"""Stubs collection"""
from typing import Annotated

from fastapi import Cookie, Header, Request

from webtronics.api.stubs.auth import AuthStub
from webtronics.api.stubs.jwt import JWTStub
from webtronics.api.stubs.poster import PosterStub
from webtronics.api.stubs.repo import PostRepoStub, UserRepoStub

__all__ = [
    'UserRepoStub',
    'PostRepoStub',
    'AuthStub',
    'JWTStub',
    'PosterStub',
    'user_repo_stub',
    'post_repo_stub',
    'auth_stub',
    'get_current_user_stub',
]


user_repo_stub = UserRepoStub()
post_repo_stub = PostRepoStub()
auth_stub = AuthStub()
poster_stub = PosterStub()


def get_current_user_stub(
    auth_header: Annotated[str | None, Header(alias='Authentication')] = None,
    auth_cookie: Annotated[str | None, Cookie(alias='access')] = None,
):
    raise NotImplementedError
