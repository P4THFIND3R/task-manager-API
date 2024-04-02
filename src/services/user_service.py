from src.api.schemas.user import User, UserSchema
from src.utils.uow import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(self, user_id: int):
        async with self.uow:
            res = await self.uow.user_repos.get_by_id(user_id)
            return res

    async def create_user(self, user: UserSchema):
        async with self.uow:
            res = await self.uow.user_repos.add_one(user.model_dump())
            return res.to_read_model()
