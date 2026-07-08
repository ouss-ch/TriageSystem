"""Import all ORM models so Base.metadata knows about every table.

TicketAnalysis is still a field-less stub (see its TODO) — left out of
Base.metadata until fleshed out, so migrations don't create a broken
empty table for it.
"""

from app.models.base import Base
from app.models.user import User
from app.models.mailbox import MailboxSweeper
from app.models.ticket import Ticket

__all__ = ["Base", "User", "MailboxSweeper", "Ticket"]
