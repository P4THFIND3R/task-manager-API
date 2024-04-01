from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    pending = "pending"
    planned = "planned"
    completed = "completed"
    canceled = "canceled"


class Task(BaseModel):
    title: str
    description: str | None
    status: TaskStatus = TaskStatus.pending

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    user_id: int

