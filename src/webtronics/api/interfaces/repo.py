"""Repository stub module"""
from abc import ABC, abstractmethod


class UserRepoInterface(ABC):
    """User repository stub class"""

    @abstractmethod
    async def read_one(self, email: str, *args, **kwargs):
        """Read one user"""

    @abstractmethod
    async def create(
        self, email: str, username: str, password: str, *args, **kwargs
    ):
        """Create user"""


class PostRepoInterface(ABC):
    """Post repository stub class"""

    @abstractmethod
    async def read_many(
        self, limit: int = 10, offset: int = 0, *args, **kwargs
    ):
        """Read all posts"""

    @abstractmethod
    async def read_one(self, post_id: int, *args, **kwargs):
        """Read one post"""

    @abstractmethod
    async def create(
        self, title: str, text: str, author_id: int, *args, **kwargs
    ):
        """Create post"""

    @abstractmethod
    async def patch(
        self,
        post_id: int,
        title: str | None = None,
        text: str | None = None,
        *args,
        **kwargs
    ):
        """Edit post title or content"""

    @abstractmethod
    async def delete(self, post_id: int, *args, **kwargs):
        """Delete post"""


class ReactionRepoInterface(ABC):
    @abstractmethod
    async def create(
        self, user_id: int, post_id: int, like: bool = True, *args, **kwargs
    ):
        """React to post"""

    @abstractmethod
    async def read(self, post_id: int, *args, **kwargs):
        """Get post reactions"""
