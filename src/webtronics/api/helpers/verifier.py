from webtronics.api.adapters.emailhunter import EmailHunterAPI
from webtronics.api.exceptions import VerifierError, EmailHunterError
from webtronics.api.stubs import EmailVerifierStub


class EmailVerifier(EmailVerifierStub):
    def __init__(self, api: EmailHunterAPI):
        self.api = api

    async def verify(self, email: str):
        try:
            response = await self.api.email_verifier(email)
        except EmailHunterError as exc:
            raise VerifierError(str(exc)) from exc
        return response['status'] not in ['invalid', 'disposable']