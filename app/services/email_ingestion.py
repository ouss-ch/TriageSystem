"""Fetch support emails from mailbox and persist as Ticket rows."""

import datetime
import logging
import re

from imap_tools import AND, MailBox
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decrypt_password
from app.models.mailbox import MailboxSweeper
from app.models.ticket import Ticket
from app.services.mailbox_auth import resolve_imap_host

logger = logging.getLogger(__name__)


def _matches_any(subject: str, regexes: list[str]) -> bool:
    return any(re.search(pattern, subject) for pattern in regexes)


def fetch_new_emails(db: Session, mailbox_sweeper_id: int) -> list[int]:
    """Sweep a single registered mailbox, persist subject-matching emails as tickets.

    One mailbox per call so a bad-credential or unreachable mailbox only fails
    its own task, not every other registered sweeper.

    Looks back 2x SWEEP_INTERVAL_SECONDS from now, every sweep — not "seen"
    state (would miss mail already read in the owner's own client, and mutate
    their mailbox by marking things read), and not "since last successful
    sweep" (a first sweep on an old, high-volume mailbox would otherwise mean
    fetching years of history — this is what caused overlapping sweeps to pile
    up and never finish). The 2x margin absorbs timing drift between beat
    ticks; message_id dedupe below makes the overlap harmless.

    Guarded by a Postgres advisory lock per mailbox so a still-running sweep
    (e.g. a slow IMAP server) causes the next tick to skip rather than stack.

    Returns the ids of newly created tickets.
    """
    sweeper = db.get(MailboxSweeper, mailbox_sweeper_id)
    if not sweeper:
        logger.warning("sweep skipped: mailbox_sweeper_id=%s not found", mailbox_sweeper_id)
        return []
    if not sweeper.regexes:
        logger.info("sweep skipped: %s has no regexes configured", sweeper.email)
        return []

    lock_acquired = db.execute(text("SELECT pg_try_advisory_lock(:key)"), {"key": sweeper.id}).scalar()
    if not lock_acquired:
        logger.info("sweep skipped: %s already in progress", sweeper.email)
        return []

    try:
        sweep_started_at = datetime.datetime.now(datetime.timezone.utc)
        since = sweep_started_at - datetime.timedelta(seconds=2 * settings.SWEEP_INTERVAL_SECONDS)
        criteria = AND(date_gte=since.date())

        logger.info("sweep started: %s (since=%s)", sweeper.email, since.isoformat())

        new_ticket_ids: list[int] = []
        scanned = 0
        host = resolve_imap_host(sweeper.email)
        password = decrypt_password(sweeper.encrypted_password)

        with MailBox(host).login(sweeper.email, password) as mailbox:
            for msg in mailbox.fetch(criteria, mark_seen=False):
                scanned += 1

                # IMAP SINCE only compares dates, not times — filter to the exact window.
                if msg.date <= since:
                    continue

                if not _matches_any(msg.subject or "", sweeper.regexes):
                    continue

                message_id = msg.headers.get("message-id", (str(msg.uid),))[0]
                exists = db.scalar(select(Ticket).where(Ticket.message_id == message_id))
                if exists:
                    continue

                ticket = Ticket(
                    mailbox_sweeper_id=sweeper.id,
                    message_id=message_id,
                    sender=msg.from_,
                    subject=msg.subject,
                    body=msg.text or msg.html or "",
                    raw_headers=dict(msg.headers),
                    received_at=msg.date,
                )
                db.add(ticket)
                db.flush()
                new_ticket_ids.append(ticket.id)
                logger.info("new ticket: %s | subject=%r from=%s", sweeper.email, msg.subject, msg.from_)

        sweeper.last_synced_at = sweep_started_at
        db.commit()
        logger.info(
            "sweep finished: %s scanned=%d new_tickets=%d", sweeper.email, scanned, len(new_ticket_ids)
        )
        return new_ticket_ids
    finally:
        db.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": sweeper.id})
