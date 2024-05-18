from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.crud import users_crud
from api.deps import SessionDep
from core.security import create_jwt_token, verify_jwt_token
from schemes.token import Token, TokenVerify

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
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
    jwt_token = create_jwt_token(user=user)
    return Token(
        access_token=jwt_token
    )


@router.post("/login/access-token/verify")
async def verify_access_token(request: TokenVerify):
    if not verify_jwt_token(token=request.access_token):
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
    return request
