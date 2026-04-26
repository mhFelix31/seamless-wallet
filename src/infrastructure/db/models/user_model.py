from datetime import datetime, timezone, date
from uuid import uuid4

from pydantic import EmailStr
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    full_name: Mapped[str] = mapped_column()
    email: Mapped[EmailStr] = mapped_column()
    date_of_birth: Mapped[date] = mapped_column()
    password_hash: Mapped[str] = mapped_column()

    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
