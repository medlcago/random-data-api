import logging
from datetime import datetime, timedelta

import bcrypt
import jwt
from jwt import PyJWTError

from core.config import config
from models.user import User

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=plain_password.encode(), hashed_password=hashed_password.encode())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode()


def create_jwt_token(user: User) -> str:
    now = datetime.utcnow()
    payload = {
        "iat": now,
        "exp": now + timedelta(minutes=config.jwt.access_token_expire_minutes),
        "user_id": user.id
    }
    token = jwt.encode(
        payload=payload,
        key=config.jwt.secret_key,
        algorithm=config.jwt.algorithm
    )
    return token


def verify_jwt_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, key=config.jwt.secret_key, algorithms=[config.jwt.algorithm])
    except PyJWTError:
        logger.info("Invalid JWT token")
        return

    user_id = payload.get("user_id")
    if user_id is None:
        logger.info("JWT token does not contain user_id")
        return
    return user_id
