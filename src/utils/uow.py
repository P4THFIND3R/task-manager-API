from abc import ABC, abstractmethod

from src.database.db import async_session_maker
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository


class IUnitOfWork(ABC):
    user_repos: UserRepository
    task_repos: TaskRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        # repositories
        self.user_repos = UserRepository(self.session)
        self.task_repos = TaskRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
