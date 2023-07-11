import httpx
from webtronics.api.exceptions import EmailHunterError


class EmailHunterAPI:
    def __init__(self, api_key: str, url: str = 'https://api.hunter.io/v2/'):
        self.url = url
        self.api_key = api_key
        self.session = httpx.AsyncClient(base_url=self.url, params={'api_key': self.api_key})

    async def email_verifier(self, email):
        response = await self.session.get('email-verifier', params={'email': email})
        if response.status_code == 401:
            content = response.json()
            errors = [error['detail'] for error in content]
            raise EmailHunterError('; '.join(errors))
        elif response.status_code != 200:
            raise EmailHunterError('Error processing request')
        content = response.json()
        return content['data']
