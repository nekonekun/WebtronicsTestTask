"""JWT stub module"""
from datetime import timedelta


class JWTStub:
    """JWT helper stub class"""

    def create_token(
        self, data: str | dict, token_lifetime: timedelta | None = None
    ):
        """Create JWT token from data. Data considered as 'sub' if is string."""
        raise NotImplementedError

    def extract_sub(self, encrypted_payload: str):
        """Extract 'sub' field from JWT token"""
        raise NotImplementedError

    def __call__(self):
        """Make class Depends-able"""
        return self
