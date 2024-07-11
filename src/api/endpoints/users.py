from fastapi import APIRouter, Depends

from src.api.endpoints.celery_router import test as celery_test
from src.auth.router import authorize

# router = APIRouter(tags=["users"], prefix="/users", dependencies=[Depends(authorize)])
router = APIRouter(tags=["users"], prefix="/users")


@router.get("/ping")
def test():
    return "pong"


@router.get("/test")
def test2():
    celery_test.delay()
    return 200
