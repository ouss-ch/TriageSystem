"""Aggregates all v1 endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import tickets, analysis, metrics, sweepers, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(sweepers.router, prefix="/sweepers", tags=["sweepers"])
