from redis import Redis
import json

from src.config import settings
from .schemas import SessionToRedis, Session
from .db import get_redis


def add_session(user: str, refresh_token: str, session: Session, cache: Redis = get_redis()):
    # canceling all user sessions if there are more than 5 active sessions
    if cache.hlen(user) > settings.USER_MAX_ACTIVE_SESSIONS:
        cache.delete(user)
        print("Очищены все сессии пользователя {}".format(user))

    cache.hset(user, refresh_token, session.model_dump_json())


def get_user_sessions(user: str, cache: Redis = get_redis()) -> dict[str: Session]:
    sessions = cache.hgetall(user)
    if sessions:
        for k, v in sessions.items():
            sessions[k] = Session(**json.loads(v))
    return sessions
