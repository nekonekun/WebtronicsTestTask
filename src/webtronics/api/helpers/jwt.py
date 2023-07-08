"""JWT-related module"""
from datetime import timedelta, datetime
from jose import jwt, JWTError

from webtronics.api.stubs import JWTStub
from webtronics.api.exceptions import JWTHelperException


DEFAULT_TOKEN_LIFE_TIME = timedelta(days=7)


class JWTHelper(JWTStub):
    """JWT helper class"""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = 'HS256',
        token_lifetime: timedelta | None = None,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_lifetime = token_lifetime or DEFAULT_TOKEN_LIFE_TIME

    def create_token(self, data: str | dict, token_lifetime: timedelta = None):
        """Create JWT token from data. Data considered as 'sub' if is string."""
        if not data:
            raise JWTHelperException('No data was provided')
        if not token_lifetime:
            token_lifetime = self.token_lifetime
        if token_lifetime < timedelta():
            raise JWTHelperException('Expires delta must be above zero')
        if isinstance(data, str):
            to_encode = {'sub': data}
        else:
            to_encode = data
        expire = datetime.utcnow() + token_lifetime
        to_encode.update({'exp': expire})
        try:
            encoded_jwt = jwt.encode(
                to_encode, self.secret_key, algorithm=self.algorithm
            )
        except JWTError as exc:
            raise JWTHelperException(
                f'Failed to create JWT. ' f'Reason: {exc}'
            ) from exc
        return encoded_jwt

    def _decrypt_payload(self, encrypted_payload: str):
        """Decrypt payload from encrypted token"""
        try:
            return jwt.decode(
                encrypted_payload, self.secret_key, algorithms=[self.algorithm]
            )
        except JWTError as exc:
            raise JWTHelperException(exc) from exc

    def extract_sub(self, encrypted_payload: str):
        """Get username from token"""
        payload = self._decrypt_payload(encrypted_payload)
        username = payload.get('sub')
        return username
