from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Annotated


class Session(BaseModel):
    id: int | str
    username: str
    fingerprint: str
    exp_at: Annotated[float, 'datetime.timestamp()']
    created_at: Annotated[float | datetime, 'datetime.timestamp(), datetime'] = datetime.now()


class Payload(BaseModel):
    username: str
    jwt_exp: float


class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str
