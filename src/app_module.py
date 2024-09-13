from nest.core import PyNestFactory, Module

from .auth.auth_bearer import JWTBearer
from .config import config, ANONYMIZE_ROUTES
from .app_controller import AppController
from .app_service import AppService
from src.users.users_module import UsersModule
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer


@Module(imports=[UsersModule], controllers=[AppController], providers=[AppService])
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This is my Async PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
    dependencies=[Depends(JWTBearer(exclude_routes=ANONYMIZE_ROUTES))]
)
http_server = app.get_server()
origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:3001",
    "localhost:3001",
]

app.use(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@http_server.on_event("startup")
async def startup():
    await config.create_all()
