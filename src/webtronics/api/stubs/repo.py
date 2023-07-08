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
