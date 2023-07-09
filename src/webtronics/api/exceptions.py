"""Errors collection"""


class AuthError(Exception):
    """Generic auth exception"""


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
