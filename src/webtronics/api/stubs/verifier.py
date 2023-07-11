class EmailVerifierStub:
    async def verify(self, email: str):
        """Pre-signup email verification"""
        raise NotImplementedError
