"""User-related schemas"""
# pylint: disable=no-name-in-module,missing-class-docstring,too-few-public-methods
from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    email: str


class UserDTO(BaseUser):
    username: str
    hashed_password: str = Field(..., hidden_from_schema=True)


class User(BaseUser):
    username: str


class UserSignUpRequest(BaseUser):
    username: str = ''
    password: str


class UserSignInRequest(BaseUser):
    password: str


class UserSignInResponse(User):
    jwt_token: str
