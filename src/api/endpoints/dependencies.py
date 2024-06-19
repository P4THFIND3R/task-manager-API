from typing import Annotated

from fastapi import Depends

from src.services.task_service import TaskService
from src.services.user_service import UserService
from src.utils.uow import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)


def get_task_service(uow: UOWDep) -> TaskService:
    return TaskService(uow)


user_service_dep = Annotated[UserService, Depends(get_user_service)]
task_service_dep = Annotated[TaskService, Depends(get_task_service)]
