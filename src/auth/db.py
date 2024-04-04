import redis.asyncio.client as redis
from src.config import settings


async def create_redis_pool():
    return redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )


pool = create_redis_pool()
