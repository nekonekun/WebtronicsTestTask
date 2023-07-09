"""Repository related module"""
from sqlalchemy import delete, select, update, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from webtronics.api.exceptions import RepoError
from webtronics.api.schemas.posts import PostDTO
from webtronics.api.schemas.users import UserDTO
from webtronics.api.stubs import PostRepoStub, UserRepoStub, ReactionRepoStub
from webtronics.db.models import Post as DbPost
from webtronics.db.models import Reaction as DbReaction
from webtronics.db.models import User as DbUser


class UserRepo(UserRepoStub):
    """User repository"""

    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker

    async def read_one(
        self, email: str, *args, session: AsyncSession | None = None, **kwargs
    ) -> UserDTO | None:
        current_session = session if session else self.sessionmaker()

        stmt = select(DbUser).where(DbUser.email == email)
        response = await current_session.execute(stmt)
        user: DbUser = response.scalars().first()

        if not session:
            await current_session.close()

        if not user:
            return None

        return UserDTO(
            id=user.id,
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
            if not session:
                await current_session.close()
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
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )


class PostRepo(PostRepoStub):
    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker

    async def create(
        self,
        title: str,
        text: str,
        author_id: int,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        current_session = session if session else self.sessionmaker()
        stmt = insert(DbPost)
        stmt = stmt.values(title=title, text=text, author_id=author_id)
        stmt = stmt.returning(DbPost)
        stmt = stmt.options(selectinload(DbPost.author))
        response = await current_session.execute(stmt)

        post: DbPost = response.scalars().first()
        stmt = insert(DbReaction)
        stmt = stmt.values(user_id=author_id, post_id=post.id, like=True)
        await current_session.execute(stmt)
        user: DbUser = post.author

        if not session:
            await current_session.commit()
            await current_session.close()

        author = UserDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )
        return PostDTO(
            id=post.id,
            title=post.title,
            text=post.text,
            author_id=post.author_id,
            author=author,
        )

    async def read_one(
        self,
        post_id: int,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        current_session = session if session else self.sessionmaker()

        stmt = select(DbPost)
        stmt = stmt.where(DbPost.id == post_id)
        stmt = stmt.options(selectinload(DbPost.author))
        response = await current_session.execute(stmt)
        if not session:
            await current_session.close()
        post: DbPost = response.scalars().first()
        if not post:
            return None

        user: DbUser = post.author

        author = UserDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )

        return PostDTO(
            id=post.id,
            title=post.title,
            text=post.text,
            author_id=post.author_id,
            author=author,
        )

    async def read_many(
        self,
        limit: int = 10,
        offset: int = 0,
        *args,
        author_id: int | None = None,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        current_session = session if session else self.sessionmaker()

        stmt = select(DbPost)
        if author_id:
            stmt = stmt.where(DbPost.author_id == author_id)
        stmt = stmt.offset(offset).limit(limit)
        stmt = stmt.options(selectinload(DbPost.author))
        stmt = stmt.order_by(DbPost.id)
        response = await current_session.execute(stmt)

        if not session:
            await current_session.close()

        posts: list[DbPost] = response.scalars().all()

        answer = []
        for post in posts:
            user: DbUser = post.author
            author = UserDTO(
                id=user.id,
                email=user.email,
                username=user.username,
                hashed_password=user.password,
            )

            answer.append(
                PostDTO(
                    id=post.id,
                    title=post.title,
                    text=post.text,
                    author_id=post.author_id,
                    author=author,
                )
            )
        return answer

    async def patch(
        self,
        post_id: int,
        title: str | None,
        text: str | None,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        current_session = session if session else self.sessionmaker()
        stmt = update(DbPost)
        stmt = stmt.where(DbPost.id == post_id)
        if title:
            stmt = stmt.values(title=title)
        if text:
            stmt = stmt.values(title=text)
        stmt = stmt.returning(DbPost)
        stmt = stmt.options(selectinload(DbPost.author))
        response = await current_session.execute(stmt)
        if not session:
            await current_session.commit()
            await current_session.close()
        post: DbPost = response.scalars().first()
        if not post:
            return None
        user: DbUser = post.author

        author = UserDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )
        return PostDTO(
            id=post.id,
            title=post.title,
            text=post.text,
            author_id=post.author_id,
            author=author,
        )

    async def delete(
        self,
        post_id: int,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        current_session = session if session else self.sessionmaker()

        stmt = delete(DbPost)
        stmt = stmt.where(DbPost.id == post_id)
        stmt = stmt.returning(DbPost)
        stmt = stmt.options(selectinload(DbPost.author))
        response = await current_session.execute(stmt)
        if not session:
            await current_session.commit()
            await current_session.close()

        post: DbPost = response.scalars().first()
        if not post:
            return None
        user: DbUser = post.author

        author = UserDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )
        return PostDTO(
            id=post.id,
            title=post.title,
            text=post.text,
            author_id=post.author_id,
            author=author,
        )


class ReactionRepo(ReactionRepoStub):
    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker

    async def create(
        self,
        user_id: int,
        post_id: int,
        like: bool = True,
        *args,
        session: AsyncSession | None = None,
        **kwargs,
    ):
        current_session = session if session else self.sessionmaker()

        stmt = insert(DbReaction)
        stmt = stmt.values(user_id=user_id, post_id=post_id, like=like)
        stmt = stmt.on_conflict_do_update(
            index_elements=['user_id', 'post_id'], set_={'like': like}
        )
        await current_session.execute(stmt)
        stmt = select(DbReaction.like)
        stmt = stmt.where(DbReaction.post_id == post_id)
        response = await current_session.execute(stmt)

        if not session:
            await current_session.commit()
            await current_session.close()

        result = response.scalars().all()
        likes = result.count(True)
        dislikes = result.count(False)

        return {'likes': likes, 'dislikes': dislikes}
