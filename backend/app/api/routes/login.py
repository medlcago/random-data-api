import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.crud import users_crud
from api.deps import SessionDep, HttpBearer
from core.security import create_token, verify_jwt_token
from schemes.token import TokenInfo, TokenVerify

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/login/access-token", response_model=TokenInfo)
async def login_access_token(
        session: SessionDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await users_crud.authenticate(session=session, username=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid login or password"
        )
    access = create_token(user_id=user.id, token_type="access")
    refresh = create_token(user_id=user.id, token_type="refresh")
    return TokenInfo(
        access_token=access,
        refresh_token=refresh
    )


@router.post(
    "/login/refresh-token",
    response_model=TokenInfo,
    response_model_exclude_none=True
)
async def refresh_access_token(http_bearer: HttpBearer):
    exp_400 = HTTPException(
        status_code=400,
        detail="Invalid refresh token"
    )
    if (payload := verify_jwt_token(token=http_bearer.credentials)) is None:
        raise exp_400
    user_id, token_type = payload
    if token_type != "refresh":
        logger.info(f"Expected 'refresh' token, got {token_type!r}")
        raise exp_400
    access_token = create_token(user_id=user_id, token_type="access")
    return TokenInfo(
        access_token=access_token
    )


@router.post("/login/verify-token")
async def verify_token(request: TokenVerify):
    if (payload := verify_jwt_token(token=request.token)) is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
    user_id, token_type = payload
    return {
        "message": "Token is valid",
        "user_id": user_id,
        "token_type": token_type
    }
