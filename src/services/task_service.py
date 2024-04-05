from src.api.schemas.task import Task, TaskUpdate
from src.utils.uow import IUnitOfWork


class TaskService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_task(self, task_id: int):
        async with self.uow:
            res = await self.uow.task_repos.get_task(task_id)
            return res

    async def get_all_tasks(self, username: str, completed: bool):
        async with self.uow:
            res = await self.uow.task_repos.get_all(username=username)
            for task in res:
                if completed is False:
                    if task.status.value == 'completed':
                        res.remove(task)
            return res

    async def add_task(self, task: Task):
        async with self.uow:
            res = await self.uow.task_repos.add_one(task.model_dump())
            res = res.to_read_model()
            await self.uow.commit()
            return res

    async def delete_task(self, task_id: int):
        async with self.uow:
            res = await self.uow.task_repos.delete_one(task_id)
            if res:
                res = res.to_read_model()
                await self.uow.commit()
                return res
            else:
                return None

    async def update_task(self, task_id: int, task_data: TaskUpdate):
        async with self.uow:
            res = await self.uow.task_repos.update_task(task_id, status=task_data.status.value,
                                                        updated_at=task_data.updated_at)
            if res:
                res = res.to_read_model()
                await self.uow.commit()
                return res
            else:
                return None
