from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, create_jwt_token, verify_password
from models import User
from schemes.token import Token
from schemes.user import CreateUserResponse, CreateUserRequest


async def authenticate(*, session: AsyncSession, username: str, password: str) -> User | None:
    user_obj = await get_user_by_username(session=session, username=username)
    if not user_obj:
        return
    if not verify_password(plain_password=password, hashed_password=user_obj.password):
        return
    return user_obj


async def create_user(*, session: AsyncSession, request: CreateUserRequest) -> CreateUserResponse | None:
    user_obj = await get_user_by_username(session=session, username=request.username)
    if user_obj:
        return
    request.password = hash_password(password=request.password)
    user = User(**request.model_dump())
    jwt_token = create_jwt_token(user=user)
    session.add(user)
    await session.commit()
    return CreateUserResponse(
        **request.model_dump(),
        token=Token(
            access_token=jwt_token
        )
    )


async def get_user_by_username(*, session: AsyncSession, username: str) -> User | None:
    user = await session.scalar(select(User).filter_by(username=username))
    return user
