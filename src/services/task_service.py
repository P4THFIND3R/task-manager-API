from src.api.schemas.task import Task
from src.utils.uow import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_task(self, user_id: int):
        async with self.uow:
            res = await self.uow.task_repos.get_by_id(user_id)
            return res
