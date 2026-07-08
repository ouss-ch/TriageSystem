"""Celery tasks — email fetch/ingestion, one mailbox at a time."""

from sqlalchemy import select

from app.core.celery_app import celery_app
from app.db.session import SyncSessionLocal
from app.models.mailbox import MailboxSweeper
from app.services.email_ingestion import fetch_new_emails
from app.tasks.analysis_tasks import analyze_ticket_task


@celery_app.task(name="tasks.fetch_emails")
def fetch_emails_task(mailbox_sweeper_id: int):
    with SyncSessionLocal() as db:
        new_ticket_ids = fetch_new_emails(db, mailbox_sweeper_id)

    for ticket_id in new_ticket_ids:
        analyze_ticket_task.delay(ticket_id)

    return len(new_ticket_ids)


@celery_app.task(name="tasks.dispatch_sweeps")
def dispatch_sweeps_task():
    """Beat-scheduled fan-out — queues one fetch_emails_task per registered mailbox."""
    with SyncSessionLocal() as db:
        sweeper_ids = db.scalars(select(MailboxSweeper.id)).all()

    for sweeper_id in sweeper_ids:
        fetch_emails_task.delay(sweeper_id)

    return len(sweeper_ids)
