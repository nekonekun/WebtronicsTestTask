"""User-related routes"""
from typing import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException, status, Response, Header, Cookie

from webtronics.api.schemas.users import (
    User,
    UserSignUpRequest,
    UserSignInRequest,
    UserSignInResponse,
)
from webtronics.api.stubs import auth_stub, AuthStub, get_current_user_stub
from webtronics.api.exceptions import AuthError


users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@users_router.post('/signup', response_model=User, name='Sign up')
async def signup(body: UserSignUpRequest, auth: AuthStub = Depends(auth_stub)):
    """Register new user"""
    try:
        response = await auth.sign_up(
            email=body.email,
            username=body.username or body.email,
            password=body.password,
        )
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc
    return response


@users_router.post(
    '/signin', response_model=UserSignInResponse, name='Sign in'
)
async def signin(
    res: Response,
    body: UserSignInRequest,
    set_cookie: Annotated[bool, Query()] = False,
    auth: AuthStub = Depends(auth_stub),
):
    """Check credentials and generate JWT token. Optionally set 'access' cookie."""
    try:
        response = await auth.sign_in(email=body.email, password=body.password)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc
    if set_cookie:
        res.set_cookie('access', response.jwt_token)
    return response


@users_router.get('/me', response_model=User)
async def get_me(current_user: Annotated[User, Depends(get_current_user_stub)],
                 auth_header: Annotated[str, Header(alias='Authentication')] = None,
                 auth_cookie: Annotated[str, Cookie(alias='access')] = None):
    """Get currently logged-in user"""
    return current_user
