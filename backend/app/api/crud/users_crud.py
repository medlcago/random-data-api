from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, create_token, verify_password
from models import User
from schemes.token import TokenInfo
from schemes.user import CreateUserResponse, CreateUserRequest


async def authenticate(*, session: AsyncSession, email: str, password: str) -> User | None:
    user_obj = await get_by_email(session=session, email=email)
    if not user_obj:
        return
    if not verify_password(plain_password=password, hashed_password=user_obj.password):
        return
    return user_obj


async def create_user(*, session: AsyncSession, request: CreateUserRequest) -> CreateUserResponse | None:
    user_obj = await get_by_email(session=session, email=request.email)
    if user_obj:
        return
    request.password = hash_password(password=request.password)
    user = User(**request.model_dump())
    session.add(user)
    await session.commit()

    access_token = create_token(user_id=user.id, token_type="access")
    refresh_token = create_token(user_id=user.id, token_type="refresh")

    return CreateUserResponse(
        **request.model_dump(),
        token=TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )


async def get_by_email(*, session: AsyncSession, email: str) -> User | None:
    user = await session.scalar(select(User).filter_by(email=email))
    return user
