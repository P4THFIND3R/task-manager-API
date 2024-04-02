from src.repositories.base_repository import Repository
from src.database.models import Users


class UserRepository(Repository):
    model = Users
