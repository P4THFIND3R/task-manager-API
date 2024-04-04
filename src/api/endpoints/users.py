from fastapi import APIRouter, Depends

from src.auth.router import authorize

router = APIRouter(tags=["users"], prefix="/users", dependencies=[Depends(authorize)])


@router.get('/test')
def test():
    print(1)
