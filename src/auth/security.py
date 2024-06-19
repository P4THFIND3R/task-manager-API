from datetime import datetime, timedelta
from secrets import token_hex

import jwt
from fastapi import Request, Response
from passlib.context import CryptContext

from src.auth import exceptions
from src.config import settings

from .exceptions import AccessTokenExpired, TokenNotFoundError
from .schemas import Payload, Session, SessionToRedis, Tokens

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    if not pwd_context.verify(password, hashed_password):
        raise exceptions.AuthenticationError
    return True


def get_fingerprint(request: Request) -> str:
    # basic fingerprint implementation
    fingerprint = request.headers.get("user-agent")
    return fingerprint


# JWT functionality
def create_access_token(username: str):
    exp = (datetime.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES)).timestamp() - 55
    encode_data = {"username": username, "exp": exp}
    encoded_jwt = jwt.encode(encode_data, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_session(username: str, fingerprint: str):
    refresh_token = token_hex(8)

    session = Session(
        username=username,
        exp_at=(datetime.now() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS)).timestamp(),
        fingerprint=fingerprint,
        created_at=datetime.now(),
    )
    return SessionToRedis(refresh_token=refresh_token, session=session)


def set_tokens_to_cookies(response: Response, tokens: Tokens):
    response.set_cookie("access_token", tokens.access_token, httponly=True)
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True)
    return response


def get_tokens_from_cookies(request: Request):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        return Tokens(access_token=access_token, refresh_token=refresh_token)
    else:
        raise TokenNotFoundError


def check_session(session: Session, fingerprint: str):
    if session:
        if session.fingerprint != fingerprint:
            raise exceptions.TokenError
        if session.exp_at < datetime.now().timestamp():
            raise exceptions.RefreshTokenExpired
    return True


def check_access_token(access_token: str):
    if not access_token:
        raise AccessTokenExpired
    try:
        payload = jwt.decode(access_token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return Payload.model_validate(payload)
    except jwt.exceptions.DecodeError:
        raise exceptions.TokenError
    except jwt.exceptions.ExpiredSignatureError:
        raise AccessTokenExpired
