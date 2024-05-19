import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import config
from core.db import async_session_maker
from core.security import verify_jwt_token
from models import User

logger = logging.getLogger(__name__)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.api.api_v1_str}/login/access-token"
)
http_bearer = HTTPBearer()


async def get_db() -> AsyncSession:
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
HttpBearer = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    exp_401 = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    if (payload := verify_jwt_token(token=token)) is None:
        raise exp_401
    user_id, token_type = payload
    if token_type != "access":
        logger.info(f"Expected 'access' token, got {token_type!r}")
        raise exp_401

    user = await session.scalar(select(User).filter_by(id=user_id))
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=403, detail="User inactive"
        )
    return current_user


CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]


def get_current_admin_user(current_user: CurrentActiveUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Access denied"
        )
    return current_user


CurrentAdminUser = Annotated[User, Depends(get_current_admin_user)]
