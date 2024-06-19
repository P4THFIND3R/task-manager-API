from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TaskStatus(Enum):
    pending = "pending"
    planned = "planned"
    completed = "completed"
    canceled = "canceled"


class Task(BaseModel):
    title: str
    description: str | None
    status: TaskStatus = TaskStatus.pending.value

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    username: str | None = None


class TaskFromDB(Task):
    id: int | None = None


class TaskUpdate(BaseModel):
    status: TaskStatus
    updated_at: datetime = datetime.now()
