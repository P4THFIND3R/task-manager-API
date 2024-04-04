from src.api.schemas.user import User, UserSchema
from src.utils.uow import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(self, username: str):
        async with self.uow:
            res = await self.uow.user_repos.get_by_username(username)
            return res

    async def create_user(self, user: UserSchema):
        async with self.uow:
            res = await self.uow.user_repos.add_one(user.model_dump())
            res = res.to_read_model()
            await self.uow.commit()
            return res

