"""Celery application instance, used by workers and beat."""

from celery import Celery

from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

celery_app = Celery(
    "triage_system",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.analysis_tasks",
    ],
)

# Periodic fan-out: re-sweeps every registered mailbox every SWEEP_INTERVAL_SECONDS.
# Newly added mailboxes also get an immediate one-off sweep — see
# app/api/v1/endpoints/sweepers.py add_email.
celery_app.conf.beat_schedule = {
    "dispatch-mailbox-sweeps": {
        "task": "tasks.dispatch_sweeps",
        "schedule": settings.SWEEP_INTERVAL_SECONDS,
    },
}

# TODO: task routing, retry policy
