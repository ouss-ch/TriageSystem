"""Ticket ORM model — raw ingested support email."""

# TODO: fields — id, sender, subject, body, received_at, raw_headers, created_at

from app.models.base import Base


class Ticket(Base):
    __tablename__ = "tickets"
