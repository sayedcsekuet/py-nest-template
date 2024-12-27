from typing import Tuple, List

from fastapi.security import HTTPBearer, APIKeyHeader
from nest.core import PyNestFactory, Module
from starlette.authentication import BaseUser, SimpleUser
from starlette.middleware.authentication import AuthenticationMiddleware
from .config import ANONYMIZE_ROUTES
from .app_controller import AppController
from .app_service import AppService
from src.users.users_module import UsersModule
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from .auth.auth_bearer_token_backend import AuthBearerTokenBackend
from .auth.auth_api_key_backend import AuthApiKeyBackend


@Module(
    imports=[UsersModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


api_key_name = 'x-api-key'

app = PyNestFactory.create(
    AppModule,
    description="This is my Async PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
    dependencies=[Depends(HTTPBearer(auto_error=False)), Depends(APIKeyHeader(name=api_key_name, auto_error=False))]
)
http_server = app.get_server()
origins = [
    "*",
]
app.use(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.use(AuthenticationMiddleware, backend=AuthBearerTokenBackend(exclude_routes=ANONYMIZE_ROUTES))
app.use(AuthenticationMiddleware, backend=AuthApiKeyBackend(name=api_key_name, exclude_routes=ANONYMIZE_ROUTES))


@http_server.on_event("startup")
async def startup():
    await config.create_all()
