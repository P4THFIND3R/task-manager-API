from src.database.models import Users
from src.repositories.base_repository import Repository


class UserRepository(Repository):
    model = Users
