from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select

from api.deps import SessionDep, get_current_admin_user
from models import User
from schemes.user import ReadUserResponse

router = APIRouter()


@router.get("/ping")
async def ping():
    return {
        "ping": "pong"
    }


@router.get(
    "/user-list",
    dependencies=[Depends(get_current_admin_user)],
    response_model=list[ReadUserResponse],
    response_model_exclude_none=True
)
async def get_user_list(
        session: SessionDep,
        limit: Annotated[int, Query(ge=1, le=10)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0
):
    statement = select(User).limit(limit=limit).offset(offset=offset)
    users = (await session.scalars(statement)).all()
    return users
