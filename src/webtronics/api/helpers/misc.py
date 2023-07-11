"""Miscellaneous dependencies"""
from typing import Annotated

from fastapi import Cookie, Header, HTTPException, status

from webtronics.api.exceptions import JWTHelperError, RepoError
from webtronics.api.interfaces import JWTInterface, UserRepoInterface
from webtronics.api.schemas.users import User


def get_current_user_factory(
    user_repo: UserRepoInterface, jwt_helper: JWTInterface
):
    """Generate get_current_user function for authorization"""

    async def get_current_user(
        auth_header: Annotated[
            str | None, Header(alias='Authentication')
        ] = None,
        auth_cookie: Annotated[str | None, Cookie(alias='access')] = None,
    ):

        if auth_header:
            token = auth_header.replace('Bearer ', '')
        else:
            if auth_cookie:
                token = auth_cookie
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED
                ) from None
        try:
            email = jwt_helper.extract_sub(token)
        except JWTHelperError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            ) from None
        try:
            user = await user_repo.read_one(email)
        except RepoError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            ) from None
        return User.parse_obj(user)

    return get_current_user
