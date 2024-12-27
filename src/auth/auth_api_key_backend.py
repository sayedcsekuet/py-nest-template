# Authentication Backend Class
import os
import re
from typing import List

from fastapi import HTTPException
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    UnauthenticatedUser,
)
from starlette.requests import HTTPConnection

from src.helper.roles import ROLE_API_USER
from src.models.user import User


class AuthApiKeyBackend(AuthenticationBackend):
    def __init__(self, name: str, exclude_routes=None, api_keys: List[str] = None):
        if exclude_routes is None:
            exclude_routes = []
        self._exclude_routes = exclude_routes
        self._name = name
        self._api_keys = api_keys or os.environ.get("API_KEYS").split(",")

    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """

    async def authenticate(self, conn: HTTPConnection):
        # This function is inherited from the base class and called by some other class
        anno = UnauthenticatedUser()
        if self._name not in conn.headers:
            return AuthCredentials(scopes=[]), anno
        for pattern in self._exclude_routes:
            if re.match(pattern, conn.url.path):
                return AuthCredentials(scopes=[]), anno
        try:
            auth_header = conn.headers[self._name]
            key = auth_header.split(" ")[-1]
            if not key or key not in self._api_keys:
                raise HTTPException(status_code=401, detail="Authorization token missing")
            roles = [ROLE_API_USER]
            user = User(unique_name=key, roles=roles)
            return AuthCredentials(scopes=roles), user
        except Exception as exception:
            raise AuthenticationError(exception) from None
