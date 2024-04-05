from fastapi import APIRouter, Depends

from src.auth.router import authorize
from src.api.schemas.task import Task, TaskFromDB, TaskUpdate
from .dependencies import task_service_dep
from ...auth.schemas import Payload

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get('/')
async def get_task(task_id: int, task_service: task_service_dep, user: str = Depends(authorize)):
    result = await task_service.get_task(task_id)
    return result


@router.get('/{username}')
async def get_all_tasks(username: str, task_service: task_service_dep, completed: bool = False,
                        user: str = Depends(authorize)):
    result = await task_service.get_all_tasks(username, completed)
    return result


@router.post('/')
async def add_task(task_data: Task, task_service: task_service_dep, user: Payload = Depends(authorize)):
    if not task_data.username:
        task_data.username = user.username
    task_data.status = task_data.status.value
    result: TaskFromDB = await task_service.add_task(task_data)
    return result


@router.delete('/')
async def delete_task(task_id: int, task_service: task_service_dep, user: Payload = Depends(authorize)):
    result: TaskFromDB = await task_service.delete_task(task_id)
    if result:
        result.status = "deleted"
    return result


@router.patch('/')
async def update_task(task_id: int, task_data: TaskUpdate, task_service: task_service_dep,
                      user: Payload = Depends(authorize)):
    result: TaskFromDB = await task_service.update_task(task_id, task_data)
    return result
