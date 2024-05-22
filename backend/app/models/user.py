from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    telegram: Mapped[str | None]
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="0")
    is_active: Mapped[bool] = mapped_column(default=True, server_default="1")
    is_blocked: Mapped[bool] = mapped_column(default=False, server_default="0")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
