"""TicketAnalysis ORM model — LLM output for a ticket (sentiment, category, keywords, priority)."""

# TODO: fields — id, ticket_id (FK), sentiment, category, keywords (JSON/array),
#       priority, llm_model, created_at

from app.models.base import Base


class TicketAnalysis(Base):
    __tablename__ = "ticket_analyses"
