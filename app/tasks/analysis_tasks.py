"""Celery tasks — run LLM analysis on a single ticket."""

from app.core.celery_app import celery_app

# TODO: call app.services.sentiment_analysis.process_ticket


@celery_app.task(name="tasks.analyze_ticket")
def analyze_ticket_task(ticket_id: int):
    raise NotImplementedError
