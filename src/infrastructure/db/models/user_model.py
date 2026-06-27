from datetime import date, datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    full_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    date_of_birth: Mapped[date] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(String(16))

    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
