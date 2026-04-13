
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    uuid: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

