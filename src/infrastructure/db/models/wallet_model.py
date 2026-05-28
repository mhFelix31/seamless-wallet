from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.base import Base


class WalletModel(Base):
    __tablename__ = "wallets"

    uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
