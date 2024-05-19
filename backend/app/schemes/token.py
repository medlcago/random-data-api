from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str | None = None


class TokenInfo(RefreshToken, AccessToken):
    token_type: str = "Bearer"


class TokenVerify(BaseModel):
    token: str
