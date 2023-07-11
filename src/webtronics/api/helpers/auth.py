"""Authentication helper module"""
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from webtronics.api.exceptions import AuthError, RepoError, AuthEmailAlreadyExistError, AuthInvalidEmail, VerifierError
from webtronics.api.schemas.users import User, UserSignInResponse
from webtronics.api.stubs import AuthStub
from webtronics.api.interfaces import JWTInterface, UserRepoInterface, EmailVerifierStub


class AuthHelper(AuthStub):
    """Authentication-related helper class"""

    def __init__(
        self,
        user_repo: UserRepoInterface,
        pwd_context: CryptContext,
        jwt_helper: JWTInterface,
        email_verifier: EmailVerifierStub | None = None
    ):
        self.pwd_context = pwd_context
        self.user_repo = user_repo
        self.jwt_helper = jwt_helper
        self.email_verifier = email_verifier

    def _verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def _verify_email(self, email: str):
        if not self.email_verifier:
            return True
        try:
            return await self.email_verifier.verify(email)
        except VerifierError:
            return True

    async def sign_up(
        self,
        email: str,
        username: str,
        password: str,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        hashed_password = self._get_password_hash(password)
        if not await self._verify_email(email):
            raise AuthInvalidEmail(f'Email "{email}" is invalid')
        try:
            user = await self.user_repo.create(
                email=email,
                username=username,
                password=hashed_password,
                session=session,
            )
        except RepoError as exc:
            raise AuthEmailAlreadyExistError(str(exc)) from exc

        return User(id=user.id, email=user.email, username=user.username)

    async def sign_in(
        self,
        email: str,
        password: str,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        try:
            user = await self.user_repo.read_one(email=email, session=session)
        except RepoError as exc:
            raise AuthError(str(exc)) from exc
        if not self._verify_password(password, user.hashed_password):
            raise AuthError('Incorrect password')
        token = self.jwt_helper.create_token(user.email)
        return UserSignInResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            jwt_token=token,
        )
