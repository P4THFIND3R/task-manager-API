# from redis import Redis
from redis.asyncio.client import Redis
from fastapi import APIRouter, Depends

from src.auth.db import pool

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


async def get_redis():
    conn_pool = await pool
    return Redis(connection_pool=conn_pool)


@router.get('/test')
async def test(redis: Redis = Depends(get_redis)):
    await redis.set('a', 'b')
    res = await redis.get('a')
    print(res)
