"""Repository related module"""
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from webtronics.api.exceptions import RepoError
from webtronics.api.schemas.users import UserDTO
from webtronics.api.stubs import UserRepoStub
from webtronics.db.models import User as DbUser


class UserRepo(UserRepoStub):
    """User repository"""

    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker

    async def read_one(
        self, email: str, *args, session: AsyncSession | None = None, **kwargs
    ) -> UserDTO:
        current_session = session if session else self.sessionmaker()

        stmt = select(DbUser).where(DbUser.email == email)
        response = await current_session.execute(stmt)
        user: DbUser = response.scalars().first()

        if not session:
            await current_session.close()

        if not user:
            return None

        return UserDTO(
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )

    async def create(
        self,
        email: str,
        username: str,
        password: str,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ) -> UserDTO:
        current_session = session if session else self.sessionmaker()

        possible_existing_user = await self.read_one(email, current_session)
        if possible_existing_user:
            raise RepoError(f'User with email {email} already exists')

        stmt = insert(DbUser).values(
            email=email, username=username, password=password
        )
        stmt = stmt.returning(DbUser)
        response = await current_session.execute(stmt)
        user: DbUser = response.scalars().first()

        if not session:
            await current_session.commit()
            await current_session.close()

        return UserDTO(
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )
