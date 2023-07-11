"""Errors collection"""


class AuthError(Exception):
    """Generic auth exception"""


class AuthInvalidEmailError(AuthError):
    """Invalid registration email"""


class AuthEmailAlreadyExistError(AuthError):
    """Email already exists"""


class JWTHelperError(Exception):
    """Generic JWT helper exception"""


class RepoError(Exception):
    """Generic Repo error"""


class PosterError(Exception):
    """Generic Poster error"""


class PosterNotFoundError(PosterError):
    """Post-not-found error"""


class PosterPermissionError(PosterError):
    """Permission-issues error"""


class EmailHunterError(Exception):
    """Generic emailhunter.co exception"""


class VerifierError(Exception):
    """Generic e-mail verifier exception"""
