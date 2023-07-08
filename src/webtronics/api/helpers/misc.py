"""Miscellaneous dependencies"""
from fastapi import Request, HTTPException, status

from webtronics.api.stubs import JWTStub, UserRepoStub
from webtronics.api.exceptions import JWTHelperException, RepoError
from webtronics.api.schemas.users import User


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
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        try:
            email = jwt_helper.extract_sub(token)
        except JWTHelperException:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        try:
            user = await user_repo.read_one(email)
        except RepoError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return User.parse_obj(user)
    return get_current_user
