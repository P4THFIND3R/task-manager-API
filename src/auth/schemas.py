from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict


class Session(BaseModel):
    username: str
    fingerprint: str
    exp_at: Annotated[float, "datetime.timestamp()"]
    created_at: Annotated[float | datetime, "datetime.timestamp(), datetime"] = datetime.now()

    model_config = ConfigDict(from_attributes=True)


class Payload(BaseModel):
    username: str
    exp: float


class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str


class SessionToRedis(BaseModel):
    refresh_token: str
    session: Session


class Tokens(BaseModel):
    access_token: str | None = None
    refresh_token: str
