"""Celery tasks — periodic email fetch/ingestion."""

from app.core.celery_app import celery_app

# TODO: call app.services.email_ingestion.fetch_new_emails, enqueue analysis_tasks per ticket


@celery_app.task(name="tasks.fetch_emails")
def fetch_emails_task():
    raise NotImplementedError
