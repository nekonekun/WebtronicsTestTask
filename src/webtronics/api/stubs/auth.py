"""Authentication helper stub module"""


class AuthStub:
    """Authentication helper stub class"""

    async def sign_up(
        self, email: str, username: str, password: str, *args, **kwargs
    ):
        """Create new user if not exists"""
        raise NotImplementedError

    async def sign_in(self, email: str, password: str, *args, **kwargs):
        """Check credentials and generate token"""
        raise NotImplementedError

    def __call__(self):
        """Make class Depends-able"""
        return self
