from webtronics.api.exceptions import (
    PosterNotFoundError,
    PosterPermissionError,
    RepoError,
)
from webtronics.api.schemas.posts import Post, PostDTO, PostReactions
from webtronics.api.schemas.users import User
from webtronics.api.stubs import PosterStub
from webtronics.api.interfaces import PostRepoInterface, ReactionRepoInterface


class PosterHelper(PosterStub):
    def __init__(self, repo: PostRepoInterface, reaction_repo: ReactionRepoInterface):
        self.repo = repo
        self.reaction_repo = reaction_repo

    async def create(
        self,
        title: str,
        text: str,
        author_id: int,
    ):
        post: PostDTO = await self.repo.create(
            title=title, text=text, author_id=author_id
        )
        author = User(
            id=post.author.id,
            email=post.author.email,
            username=post.author.username,
        )
        return Post(
            id=post.id, title=post.title, text=post.text, author=author
        )

    async def read_one(self, post_id: int):
        try:
            post: PostDTO = await self.repo.read_one(post_id=post_id)
        except RepoError as exc:
            raise PosterNotFoundError(str(exc)) from exc
        author = User(
            id=post.author.id,
            email=post.author.email,
            username=post.author.username,
        )
        return Post(
            id=post.id, title=post.title, text=post.text, author=author
        )

    async def read_many(
        self,
        author_id: int | None = None,
        limit: int = 10,
        offset: int = 0,
    ):
        posts: list[PostDTO] = await self.repo.read_many(
            author_id=author_id, limit=limit, offset=offset
        )
        if not posts:
            return []
        answer = []
        for post in posts:
            author = User(
                id=post.author.id,
                email=post.author.email,
                username=post.author.username,
            )
            answer.append(
                Post(
                    id=post.id, title=post.title, text=post.text, author=author
                )
            )
        return answer

    async def delete(self, post_id: int):
        try:
            post: PostDTO = await self.repo.delete(post_id=post_id)
        except RepoError as exc:
            raise PosterNotFoundError(str(exc)) from exc
        author = User(
            id=post.author.id,
            email=post.author.email,
            username=post.author.username,
        )
        return Post(
            id=post.id, title=post.title, text=post.text, author=author
        )

    async def patch(
        self, post_id: int, title: str | None = None, text: str | None = None
    ):
        try:
            post: PostDTO = await self.repo.patch(
                post_id=post_id, title=title, text=text
            )
        except RepoError as exc:
            raise PosterNotFoundError(str(exc)) from exc
        author = User(
            id=post.author.id,
            email=post.author.email,
            username=post.author.username,
        )
        return Post(
            id=post.id, title=post.title, text=post.text, author=author
        )

    async def react(self, post_id: int, user_id: int, like: bool = True):
        try:
            post = await self.read_one(post_id)
        except RepoError as exc:
            raise PosterNotFoundError(str(exc)) from exc
        if post.author.id == user_id:
            raise PosterPermissionError('You cannot react to own post')
        response = await self.reaction_repo.create(
            user_id=user_id, post_id=post_id, like=like
        )
        return PostReactions(post_id=post.id, **response)

    async def read_reactions(self, post_id: int):
        response = await self.reaction_repo.read(post_id=post_id)
        return PostReactions(post_id=post_id, **response)
