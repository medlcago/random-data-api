from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from schemes.token import TokenInfo


class CreateUserRequest(BaseModel):
    username: Annotated[str, Field(pattern="r^[a-zA-Z][\w]{4,31}$")]
    password: Annotated[str, Field(min_length=6)]
    telegram: Annotated[str | None, Field(pattern=r"^@[a-zA-Z][\w]{4,31}$")] = None


class CreateUserResponse(BaseModel):
    username: str
    telegram: str | None = None
    token: TokenInfo


class ReadUserResponse(BaseModel):
    id: int
    username: str
    telegram: str | None
    is_admin: bool
    is_active: bool
    is_blocked: bool
    created_at: datetime
