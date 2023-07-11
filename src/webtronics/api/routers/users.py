"""User-related routes"""
from typing import Annotated

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Query,
    Response,
    status,
)

from webtronics.api.exceptions import AuthError, AuthEmailAlreadyExistError, AuthInvalidEmail
from webtronics.api.schemas.users import (
    User,
    UserSignInRequest,
    UserSignInResponse,
    UserSignUpRequest,
)
from webtronics.api.stubs import AuthStub, auth_stub, get_current_user_stub

users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@users_router.post('/signup', response_model=User, name='Sign up')
async def signup(
    auth: Annotated[AuthStub, Depends(auth_stub)], body: UserSignUpRequest
):
    """Register new user"""
    try:
        response = await auth.sign_up(
            email=body.email,
            username=body.username or body.email,
            password=body.password,
        )
    except AuthEmailAlreadyExistError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'Email "{body.email}" already registered'
        ) from exc
    except AuthInvalidEmail as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'Email "{body.email}" seems to be invalid'
        ) from exc
    return response


@users_router.post(
    '/signin', response_model=UserSignInResponse, name='Sign in'
)
async def signin(
    res: Response,
    auth: Annotated[AuthStub, Depends(auth_stub)],
    body: UserSignInRequest,
    set_cookie: Annotated[bool, Query()] = False,
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
async def get_me(
    current_user: Annotated[User, Depends(get_current_user_stub)],
):
    """Get currently logged-in user information"""
    return current_user
