"""User-related schemas"""
# pylint: disable=no-name-in-module,missing-class-docstring,too-few-public-methods
from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str


class UserDTO(BaseUser):
    id: int
    username: str
    hashed_password: str


class User(BaseUser):
    id: int
    username: str


class UserSignUpRequest(BaseUser):
    username: str = ''
    password: str


class UserSignInRequest(BaseUser):
    password: str


class UserSignInResponse(User):
    jwt_token: str
