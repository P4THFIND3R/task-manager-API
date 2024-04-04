from typing import Annotated
from fastapi import Depends
from src.services.user_service import UserService
from src.utils.uow import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)


user_service_dep = Annotated[UserService, Depends(get_user_service)]
