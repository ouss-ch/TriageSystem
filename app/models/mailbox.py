"""MailboxSweeper ORM model — a mailbox registered for ticket-email sweeping.

Credentials are supplied per-mailbox at runtime (see app/api/v1/endpoints/sweepers.py)
instead of living in fixed EMAIL_* env vars, so multiple inboxes can be swept at once,
each with its own set of ticket-matching regexes.
"""

import datetime
from typing import Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MailboxSweeper(Base):
    __tablename__ = "mailbox_sweepers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    # Fernet-encrypted, not hashed — the sweep worker needs the plaintext back to log into IMAP.
    encrypted_password: Mapped[str] = mapped_column(String, nullable=False)
    regexes: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    # Informational only — timestamp of the last successful sweep. The sweep's
    # actual fetch window is a rolling 2x SWEEP_INTERVAL_SECONDS from "now" (see
    # app/services/email_ingestion.py), not derived from this column.
    last_synced_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
