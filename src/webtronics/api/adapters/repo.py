"""Repository related module"""
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from webtronics.api.exceptions import RepoError
from webtronics.api.schemas.posts import PostDTO
from webtronics.api.schemas.users import UserDTO
from webtronics.api.stubs import PostRepoStub, ReactionRepoStub, UserRepoStub
from webtronics.db.models import Post as DbPost
from webtronics.db.models import Reaction as DbReaction
from webtronics.db.models import User as DbUser
from redis import asyncio as aioredis


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
            raise RepoError('User not found')

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
        try:
            await self.read_one(email, current_session)
            found = True
        except RepoError:
            found = False

        if found:
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
            raise RepoError(f'Post with ID {post_id} does not exist')

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
        title: str | None = None,
        text: str | None = None,
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
            stmt = stmt.values(text=text)
        stmt = stmt.returning(DbPost)
        stmt = stmt.options(selectinload(DbPost.author))
        response = await current_session.execute(stmt)
        if not session:
            await current_session.commit()
            await current_session.close()
        post: DbPost = response.scalars().first()
        if not post:
            raise RepoError(f'Post with ID {post_id} does not exist')
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
            raise RepoError(f'Post with ID {post_id} does not exist')
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
        stmt = select(DbReaction)
        stmt = stmt.options(selectinload(DbReaction.user))
        stmt = stmt.where(DbReaction.post_id == post_id)
        response = await current_session.execute(stmt)

        if not session:
            await current_session.commit()
            await current_session.close()

        result: list[DbReaction] = response.scalars().all()
        likes = [reaction.user.id for reaction in result if reaction.like]
        dislikes = [
            reaction.user.id for reaction in result if not reaction.like
        ]

        return {'likes': likes, 'dislikes': dislikes}

    async def read(self, post_id: int, *args, session: AsyncSession | None = None, **kwargs):
        current_session = session if session else self.sessionmaker()

        stmt = select(DbReaction)
        stmt = stmt.options(selectinload(DbReaction.user))
        stmt = stmt.where(DbReaction.post_id == post_id)
        response = await current_session.execute(stmt)

        if not session:
            await current_session.close()

        result: list[DbReaction] = response.scalars().all()
        likes = [reaction.user.id for reaction in result if reaction.like]
        dislikes = [
            reaction.user.id for reaction in result if not reaction.like
        ]

        return {'likes': likes, 'dislikes': dislikes}


class ReactionRepoWithCache(ReactionRepo):
    def __init__(self, sessionmaker: async_sessionmaker, redis_client: aioredis.Redis):
        self.redis_client = redis_client
        super().__init__(sessionmaker)

    async def create(
        self, user_id: int, post_id: int, like: bool = True, *args, session: AsyncSession | None = None, **kwargs
    ):
        await super().create(user_id, post_id, like, session=session)
        like_key = f'like_{post_id}'
        dislike_key = f'dislike_{post_id}'

        if like:
            await self.redis_client.srem(dislike_key, user_id)
            await self.redis_client.sadd(like_key, user_id)
        else:
            await self.redis_client.srem(like_key, user_id)
            await self.redis_client.sadd(dislike_key, user_id)

    async def read(self, post_id: int, *args, **kwargs):
        like_key = f'like_{post_id}'
        dislike_key = f'dislike_{post_id}'
        likes = await self.redis_client.smembers(like_key)
        dislikes = await self.redis_client.smembers(dislike_key)
        return {'likes': likes, 'dislikes': dislikes}

    async def init_cache(self):
        await self.redis_client.delete('*')

        current_session = self.sessionmaker()
        stmt = select(DbReaction)
        stmt = stmt.options(selectinload(DbReaction.user))
        response = await current_session.execute(stmt)
        await current_session.close()

        result: list[DbReaction] = response.scalars().all()

        for element in result:
            post_id = element.post_id
            user_id = element.user_id
            like_key = f'like_{post_id}'
            dislike_key = f'dislike_{post_id}'
            if element.like:
                await self.redis_client.sadd(like_key, user_id)
            else:
                await self.redis_client.sadd(dislike_key, user_id)
