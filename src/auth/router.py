from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.api.schemas.user import UserSchema
import src.auth.security as security
import src.auth.exceptions as exceptions
from .schemas import Session, SessionToRedis, Tokens
from .db import pool
from .dependencies import user_service_dep, fingerprint_dep, redis_dep
from .repository import add_session

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


async def check_user(userdata: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: user_service_dep):
    user: UserSchema = await user_service.get_user(userdata.username)
    if not user:
        raise exceptions.UserNotFoundError
    security.verify_password(userdata.password, user.password)
    return user.username


@router.post('/signin')
async def signin(userdata: UserSchema, user_service: user_service_dep):
    userdata.password = security.hash_password(userdata.password)
    user = await user_service.create_user(userdata)
    return user


@router.post('/login')
async def authentication(response: Response,
                         fingerprint: fingerprint_dep, cache: redis_dep,
                         user: Annotated[str, 'username'] = Depends(check_user)):
    # create access and refresh tokens
    access_token: str = security.create_access_token(user)
    session_to_add: SessionToRedis = security.create_session(user, fingerprint)
    # add an entry to the cache
    add_session(user, session_to_add.refresh_token, session_to_add.session)

    # setting tokens in cookies
    security.set_tokens_to_cookies(response,
                                   Tokens(access_token=access_token, refresh_token=session_to_add.refresh_token))
    return {'access_token': access_token, 'refresh_token': session_to_add.refresh_token}
