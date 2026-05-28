from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.base import Base


class WalletTransactionSnapshot(Base):
    __tablename__ = "wallet_transaction_snapshot"

    uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    wallet_uuid: Mapped[str] = mapped_column(ForeignKey("wallets.uuid"))
    transaction_uuid: Mapped[str] = mapped_column(ForeignKey("transactions.uuid"))

    projected_balance: Mapped[int]
    projected_currency_id: Mapped[str] = mapped_column(ForeignKey("currencies.id"))

    snapshot_start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    snapshot_end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
