from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError


class Repository(BaseRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_username(self, username: str) -> model:
        stmt = select(self.model).where(self.model.username == username)
        result = await self.session.execute(stmt)
        result = result.first()
        if result:
            return result[0].to_read_model()

    async def add_one(self, data: dict) -> model:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_one(self, id: int) -> model:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        result = await self.session.execute(stmt)
        result = result.first()
        if result:
            return result[0]
