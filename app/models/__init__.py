"""Import all ORM models so Base.metadata knows about every table.

Ticket and TicketAnalysis are still field-less stubs (see their TODOs) —
left out of Base.metadata until fleshed out, so migrations don't create
broken empty tables for them.
"""

from app.models.base import Base
from app.models.user import User
from app.models.mailbox import MailboxSweeper

__all__ = ["Base", "User", "MailboxSweeper"]
