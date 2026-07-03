"""Pydantic schemas for aggregated dashboard metrics."""

from pydantic import BaseModel

# TODO: MetricsSummary, SentimentBreakdown, CategoryBreakdown, PriorityBreakdown


class MetricsBase(BaseModel):
    pass
