# Authentication Backend Class
import re

from azure_ad_verify_token import verify_jwt
from fastapi import HTTPException
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    UnauthenticatedUser,
)
from starlette.requests import HTTPConnection

from src.config import JWT_CONFIG
from src.helper.roles import ROLE_ADMIN, ROLES_REPORT_ADMIN
from src.models.user import User


class AuthBearerTokenBackend(AuthenticationBackend):
    def __init__(self, exclude_routes=None):
        if exclude_routes is None:
            exclude_routes = []
        self._exclude_routes = exclude_routes

    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """

    async def authenticate(self, conn: HTTPConnection):
        # This function is inherited from the base class and called by some other class
        anno = UnauthenticatedUser()
        if "Authorization" not in conn.headers:
            return AuthCredentials(scopes=[]), anno
        for pattern in self._exclude_routes:
            if re.match(pattern, conn.url.path):
                return AuthCredentials(scopes=[]), anno
        try:
            auth_header = conn.headers["Authorization"]
            token = auth_header.split(" ")[-1]  # Generic approach: "Bearer eyJsn..." -> "eyJsn...", "Access Token eyJsn..." -> "eyJsn..."
            if not token:
                raise HTTPException(status_code=401, detail="Authorization token missing")
            payload = verify_jwt(
                token=token,
                **JWT_CONFIG
            )
            user = User(**payload)
            roles = payload.get('roles', [])
            if ROLE_ADMIN in roles:
                roles.extend(ROLES_REPORT_ADMIN)
            return AuthCredentials(scopes=roles), user
        except Exception as exception:
            raise AuthenticationError(exception) from None
