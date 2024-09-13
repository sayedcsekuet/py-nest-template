from nest.core import Controller, Get, Post
from .users_service import UsersService
from .users_model import Users


@Controller("users")
class UsersController:

    def __init__(self, users_service: UsersService):
        self.users_service = users_service
    
    @Get("/")
    def get_users(self):
        return self.users_service.get_users()
        
    @Post("/")
    def add_users(self, users: Users):
        return self.users_service.add_users(users)

