from abc import ABC, abstractmethod


class EmailVerifierStub(ABC):

    @abstractmethod
    async def verify(self, email: str):
        """Pre-signup email verification"""
        raise NotImplementedError
