"""JWT stub module"""
from abc import ABC, abstractmethod
from datetime import timedelta


class JWTInterface(ABC):
    """JWT helper stub class"""

    @abstractmethod
    def create_token(
        self, data: str | dict, token_lifetime: timedelta | None = None
    ):
        """Create JWT token from data. Data considered as 'sub' if is string."""
        raise NotImplementedError

    @abstractmethod
    def extract_sub(self, encrypted_payload: str):
        """Extract 'sub' field from JWT token"""
        raise NotImplementedError
