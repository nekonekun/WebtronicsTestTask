from webtronics.api.schemas.posts import Post, PostDTO
from webtronics.api.schemas.users import User
from webtronics.api.stubs import PosterStub, PostRepoStub


class PosterHelper(PosterStub):
    def __init__(self, repo: PostRepoStub):
        self.repo = repo

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
        post: PostDTO = await self.repo.read_one(post_id=post_id)
        if not post:
            return None
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
        post: PostDTO = await self.repo.delete(post_id=post_id)
        if not post:
            return None
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
        post: PostDTO = await self.repo.patch(post_id=post_id, title=title, text=text)
        if not post:
            return None
        author = User(
            id=post.author.id,
            email=post.author.email,
            username=post.author.username,
        )
        return Post(
            id=post.id, title=post.title, text=post.text, author=author
        )