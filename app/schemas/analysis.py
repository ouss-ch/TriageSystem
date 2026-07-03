"""Pydantic schemas for TicketAnalysis (sentiment, category, keywords, priority)."""

from pydantic import BaseModel

# TODO: AnalysisRead, SentimentEnum, PriorityEnum


class AnalysisBase(BaseModel):
    pass
