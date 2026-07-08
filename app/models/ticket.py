"""Ticket ORM model — raw ingested support email, matched by a mailbox sweeper's regexes."""

import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    mailbox_sweeper_id: Mapped[int] = mapped_column(ForeignKey("mailbox_sweepers.id"), nullable=False)
    # RFC Message-ID header — stable dedupe key across repeated sweeps of the same mailbox.
    message_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    sender: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    raw_headers: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    received_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
