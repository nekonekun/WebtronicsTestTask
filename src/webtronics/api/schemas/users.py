"""User-related schemas"""
# pylint: disable=no-name-in-module,missing-class-docstring,too-few-public-methods
from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    id: int
    email: str
    username: str
    hashed_password: str


class User(BaseModel):
    id: int = Field(examples=[0], description='User ID')
    email: str = Field(examples=['email@local'], description='Email')
    username: str = Field(examples=['username'], description='Username')


class UserSignUpRequest(BaseModel):
    email: str = Field(examples=['email@local'], description='Email (must be unique)')
    username: str = Field(examples=['username'], description='Username')
    password: str = Field(examples=['password'], description='Password')


class UserSignInRequest(BaseModel):
    email: str = Field(examples=['email@local'], description='Email')
    password: str = Field(examples=['password'], description='Password')


class UserSignInResponse(User):
    jwt_token: str = Field('jwt_authentication_token', description='JWT authentication token')
