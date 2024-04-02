from fastapi import APIRouter, Depends
from typing import Annotated

from src.api.schemas.user import UserSchema
from src.utils.uow import IUnitOfWork, UnitOfWork
from src.services.user_service import UserService

router = APIRouter(tags=["users"], prefix="/users")


@router.get("")
async def get_user(us_id: int, uow: Annotated[IUnitOfWork, Depends(UnitOfWork)]):
    user_service = UserService(uow)
    res = await user_service.get_user(us_id)
    return res


@router.post("")
async def add_user(user: UserSchema, uow: Annotated[IUnitOfWork, Depends(UnitOfWork)]):
    user_service = UserService(uow)
    res = await user_service.create_user(user)
    return res
