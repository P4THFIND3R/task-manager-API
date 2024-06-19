from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

import src.auth.exceptions as exceptions
import src.auth.security as security
from src.api.schemas.user import UserSchema
from src.log.logger import logger

from .dependencies import fingerprint_dep, user_service_dep
from .repository import add_session, get_session
from .schemas import Payload, Session, SessionToRedis, Tokens

router = APIRouter(prefix="/auth", tags=["Authentication"])


async def check_user(userdata: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: user_service_dep):
    user: UserSchema = await user_service.get_user(userdata.username)
    if not user:
        raise exceptions.UserNotFoundError
    security.verify_password(userdata.password, user.password)
    return user.username


@router.post("/signin")
async def signin(userdata: UserSchema, user_service: user_service_dep):
    userdata.password = security.hash_password(userdata.password)
    user = await user_service.create_user(userdata)
    return user


@router.post("/login")
async def authentication(
    response: Response, fingerprint: fingerprint_dep, user: Annotated[str, "username"] = Depends(check_user)
):
    # create access and refresh tokens
    access_token: str = security.create_access_token(user)
    session_to_add: SessionToRedis = security.create_session(user, fingerprint)
    # add an entry to the cache
    add_session(user, session_to_add.refresh_token, session_to_add.session)

    # setting tokens in cookies
    security.set_tokens_to_cookies(
        response, Tokens(access_token=access_token, refresh_token=session_to_add.refresh_token)
    )
    return Tokens(**{"access_token": access_token, "refresh_token": session_to_add.refresh_token})


@router.post("/update")
async def update_tokens(request: Request, response: Response, fingerprint: fingerprint_dep):
    # get tokens from cookies, we are only interested in refresh_token, access_token may be missing
    tokens: Tokens = security.get_tokens_from_cookies(request)
    # get session by refresh token
    session: Session = get_session(tokens.refresh_token)
    if session:
        # check if session is valid and not expired
        security.check_session(session, fingerprint=fingerprint)

        tokens: Tokens = await authentication(response, fingerprint, session.username)
        logger.debug("Tokens updated successfully!")
        return tokens
    else:
        raise exceptions.RefreshTokenExpired


@router.post("/authorize")
async def authorize(request: Request, response: Response, fingerprint: fingerprint_dep):
    # get tokens from cookies
    tokens: Tokens = security.get_tokens_from_cookies(request)
    try:
        payload: Payload = security.check_access_token(tokens.access_token)
    except exceptions.AccessTokenExpired:
        tokens = await update_tokens(request, response, fingerprint)
        payload: Payload = security.check_access_token(tokens.access_token)
    return Payload.model_validate(payload)
