"""Repository stub module"""


class UserRepoStub:
    """User repository stub class"""

    async def read_one(self, email: str, *args, **kwargs):
        """Read one user"""
        raise NotImplementedError

    async def create(
        self, email: str, username: str, password: str, *args, **kwargs
    ):
        """Create user"""
        raise NotImplementedError

    def __call__(self):
        """Make class Depends-able"""
        return self


class PostRepoStub:
    """Post repository stub class"""

    async def read_many(
        self, limit: int = 10, offset: int = 0, *args, **kwargs
    ):
        """Read all posts"""
        raise NotImplementedError

    async def read_one(self, post_id: int, *args, **kwargs):
        """Read one post"""
        raise NotImplementedError

    async def create(
        self, title: str, text: str, author_id: int, *args, **kwargs
    ):
        """Create post"""
        raise NotImplementedError

    async def patch(
        self, post_id: int, title: str | None, text: str | None, *args, **kwargs
    ):
        """Edit post title or content"""
        raise NotImplementedError

    async def delete(self, post_id: int, *args, **kwargs):
        """Delete post"""
        raise NotImplementedError

    def __call__(self):
        """Make class Depends-able"""
        return self
