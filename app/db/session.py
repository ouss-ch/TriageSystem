"""SQLAlchemy engines / session factories.

Two engines on purpose: the API is async (asyncpg), but Celery workers are
plain sync processes — sharing one asyncio event loop across prefork worker
processes isn't worth the complexity, so tasks get a sync (psycopg2) engine
instead.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

sync_engine = create_engine(settings.DATABASE_URL.replace("+asyncpg", ""), echo=settings.DEBUG)
SyncSessionLocal = sessionmaker(sync_engine, expire_on_commit=False)


async def get_db():
    # TODO: yield session, handle commit/rollback
    async with AsyncSessionLocal() as session:
        yield session
