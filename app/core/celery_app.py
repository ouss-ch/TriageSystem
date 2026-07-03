"""Celery application instance, used by workers and beat."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "triage_system",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.analysis_tasks",
    ],
)

# TODO: task routing, retry policy, beat schedule
