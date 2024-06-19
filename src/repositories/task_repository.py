import datetime

from sqlalchemy import insert, select, update

from src.database.models import Tasks
from src.repositories.base_repository import Repository


class TaskRepository(Repository):
    model = Tasks

    async def get_all(self, username: str | None = None):
        stmt = select(self.model)
        if username:
            stmt = stmt.where(self.model.username == username)
        result = await self.session.execute(stmt)
        return [task.to_read_model() for task in result.scalars().all()]

    async def get_task(self, task_id: int):
        stmt = select(self.model).where(self.model.id == task_id)
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        if result:
            return result.to_read_model()

    async def update_task(self, task_id: int, status: str, updated_at: datetime.datetime):
        stmt = (
            update(self.model)
            .values(status=status, updated_at=updated_at)
            .where(self.model.id == task_id)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        if result:
            return result
