from typing import Annotated
from fastapi import Depends
from src.services.user_service import UserService
from src.utils.uow import IUnitOfWork, UnitOfWork
from redis import Redis
from .db import get_redis

from src.auth import security

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)


user_service_dep = Annotated[UserService, Depends(get_user_service)]
fingerprint_dep = Annotated[str, Depends(security.get_fingerprint)]
redis_dep = Annotated[Redis, Depends(get_redis)]
