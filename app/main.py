"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health() -> dict:
    # TODO: add DB / broker connectivity checks
    return {"status": "ok"}
