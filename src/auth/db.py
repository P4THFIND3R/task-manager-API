from redis import Redis, ConnectionPool
from src.config import settings


def create_redis_pool():
    return ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
        max_connections=10
    )


pool = create_redis_pool()


def get_redis() -> Redis:
    return Redis(connection_pool=pool)
