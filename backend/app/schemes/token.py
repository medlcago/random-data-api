from pydantic import BaseModel

from core.config import config


class Token(BaseModel):
    access_token: str
    lifetime: int = config.jwt.access_token_expire_minutes


class TokenVerify(BaseModel):
    access_token: str
