import logging

from fastapi import APIRouter, HTTPException

from api.crud import users_crud
from core.config import config
from api.deps import SessionDep, CurrentUser
from schemes.user import CreateUserRequest, CreateUserResponse, ReadUserResponse

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/",
             response_model=CreateUserResponse,
             response_model_exclude_none=True,
             status_code=201,
             summary="User registration"
             )
async def create_user(session: SessionDep, data: CreateUserRequest):
    if not config.api.users_open_registration:
        logger.warning("Open user registration is disabled")
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server.",
        )

    user = await users_crud.create_user(
        session=session,
        request=data
    )
    if user is None:
        logger.info(f"User with username {data.username!r} already exists.")
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return user


@router.get("/me",
            response_model=ReadUserResponse,
            response_model_exclude_none=True,
            summary="About me"
            )
async def get_me(current_user: CurrentUser):
    return current_user
