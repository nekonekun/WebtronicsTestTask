class PosterStub:
    async def create(self, title: str, text: str, author_id: int):
        """Create new post"""
        raise NotImplementedError

    async def read_one(self, post_id: int):
        """Read one post"""
        raise NotImplementedError

    async def read_many(
        self,
        author_id: int | None = None,
        limit: int = 10,
        offset: int = 0,
    ):
        """Filter posts"""
        raise NotImplementedError

    async def patch(
        self, post_id: int, title: str | None = None, text: str | None = None
    ):
        """Edit post title or text"""
        raise NotImplementedError

    async def delete(self, post_id: int):
        """Delete post"""
        raise NotImplementedError

    def __call__(self):
        """Make class Depends-able"""
        return self
