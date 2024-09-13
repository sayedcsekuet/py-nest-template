from .users_model import Users
from nest.core import Injectable


@Injectable
class UsersService:

    def __init__(self):
        self.database = []
        
    def get_users(self):
        return self.database
    
    def add_users(self, users: Users):
        self.database.append(users)
        return users
