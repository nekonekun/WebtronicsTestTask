"""Miscellaneous dependencies"""
from fastapi import HTTPException, Request, status

from webtronics.api.exceptions import JWTHelperError, RepoError
from webtronics.api.schemas.users import User
from webtronics.api.stubs import JWTStub, UserRepoStub


def get_current_user_factory(user_repo: UserRepoStub, jwt_helper: JWTStub):
    async def get_current_user(req: Request):
        authentication_header = req.headers.get('Authentication')
        if authentication_header:
            token = authentication_header.replace('Bearer ', '')
        else:
            access_cookie = req.cookies.get('access')
            if access_cookie:
                token = access_cookie
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
