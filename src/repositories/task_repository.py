from src.repositories.base_repository import Repository
from src.database.models import Tasks


class TaskRepository(Repository):
    model = Tasks
