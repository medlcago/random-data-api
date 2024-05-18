import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Depends

from utils import UserUtil

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/user-info")
async def generate_random_user_info(
        user_util: Annotated[UserUtil, Depends(UserUtil)],
        locale: str | None = None,
        n: Annotated[int, Query(ge=1, le=10)] = 1
):
    try:
        return user_util.generate_user_info(locale=locale, n=n)
    except AttributeError as ex:
        logger.info(ex)
        raise HTTPException(
            status_code=400,
            detail="Invalid locale."
        )


@router.get("/user-profile")
async def generate_random_user_profile(
        user_util: Annotated[UserUtil, Depends(UserUtil)],
        locale: str | None = None,
        n: Annotated[int, Query(ge=1, le=10)] = 1,
        simple: bool = True
):
    try:
        return user_util.generate_user_profile(locale=locale, n=n, simple=simple)
    except AttributeError as ex:
        logger.info(ex)
        raise HTTPException(
            status_code=400,
            detail="Invalid locale."
        )
