import logging
from datetime import datetime, timedelta

import bcrypt
import jwt
from jwt import PyJWTError

from core.config import config

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=plain_password.encode(), hashed_password=hashed_password.encode())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode()


def create_token(user_id: int, token_type: str = "access", lifetime_minutes: int | None = None) -> str:
    now = datetime.utcnow()
    if lifetime_minutes is None:
        if token_type == "access":
            lifetime_minutes = config.jwt.access_token_expire_minutes
        else:
            lifetime_minutes = config.jwt.refresh_token_expire_minutes
    payload = {
        "iat": now,
        "exp": now + timedelta(minutes=lifetime_minutes),
        "user_id": user_id,
        "type": token_type,
    }
    token = jwt.encode(
        payload=payload,
        key=config.jwt.secret_key,
        algorithm=config.jwt.algorithm
    )
    return token


def verify_jwt_token(token: str) -> tuple[int, str] | None:
    try:
        payload = jwt.decode(token, key=config.jwt.secret_key, algorithms=[config.jwt.algorithm])
    except PyJWTError:
        logger.info("Failed to decode token")
        return

    user_id = payload.get("user_id")
    token_type = payload.get("type")
    if user_id is not None and token_type is not None:
        return user_id, token_type
    else:
        logger.info("Invalid token")
        return
