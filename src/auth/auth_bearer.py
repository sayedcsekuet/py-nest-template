import re

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from azure_ad_verify_token import verify_jwt

from src.config import JWT_CONFIG


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, exclude_routes: list = None):
        if exclude_routes is None:
            exclude_routes = []
        self._exclude_routes = exclude_routes
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        for pattern in self._exclude_routes:
            if re.match(pattern, request.url.path):
                return None
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = verify_jwt(
                token=token,
                **JWT_CONFIG
            )
        except:
            payload = None
        if payload:
            is_token_valid = True

        return is_token_valid
