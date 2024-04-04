from redis.asyncio.client import Redis
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.api.schemas.user import UserSchema
import src.auth.security as security
import src.auth.exceptions as exceptions
from .db import pool
from .dependencies import user_service_dep

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


async def get_redis():
    conn_pool = await pool
    return Redis(connection_pool=conn_pool)


async def check_user(userdata: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: user_service_dep):
    user: UserSchema = await user_service.get_user(userdata.username)
    if not user:
        raise exceptions.UserNotFoundError
    security.verify_password(userdata.password, user.password)
    return user.username


@router.get('/test')
async def test(user=Depends(check_user)):
    return user


@router.post('/signin')
async def signin(userdata: UserSchema, user_service: user_service_dep):
    userdata.password = security.hash_password(userdata.password)
    user = await user_service.create_user(userdata)
    return user
