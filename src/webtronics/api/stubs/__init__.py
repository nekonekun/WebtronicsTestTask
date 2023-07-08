"""Stubs collection"""
from fastapi import Request
from webtronics.api.stubs.repo import UserRepoStub
from webtronics.api.stubs.auth import AuthStub
from webtronics.api.stubs.jwt import JWTStub

user_repo_stub = UserRepoStub()
auth_stub = AuthStub()


def get_current_user_stub(req: Request):
    raise NotImplementedError


__all__ = [
    'UserRepoStub',
    'AuthStub',
    'JWTStub',
    'user_repo_stub',
    'auth_stub',
    'get_current_user_stub'
]
