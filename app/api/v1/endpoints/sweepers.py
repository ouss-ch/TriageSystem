"""Mailbox sweeper endpoints.

Manages which mailboxes get swept for support-ticket emails and which regexes
identify a sweepable ticket in each one. Credentials are supplied per-mailbox
here rather than fixed EMAIL_* env vars, so multiple inboxes can be registered.

Every route here requires an authenticated admin account (see app/api/deps.py).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_admin
from app.core.security import encrypt_password
from app.models.mailbox import MailboxSweeper
from app.schemas.mailbox import (
    SweeperCreateRequest,
    SweeperCreateResponse,
    SweeperRead,
    SweeperRegexUpdateRequest,
    SweeperRemoveResponse,
)
from app.services.mailbox_auth import verify_imap_credentials

router = APIRouter(dependencies=[Depends(require_admin)])


@router.post("/", response_model=SweeperCreateResponse)
async def add_email(payload: SweeperCreateRequest, db: AsyncSession = Depends(get_db)):
    if not verify_imap_credentials(payload.email, payload.password):
        return SweeperCreateResponse(success=False, message="credentials incorrect")

    existing = await db.scalar(select(MailboxSweeper).where(MailboxSweeper.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="email already registered")

    sweeper = MailboxSweeper(
        email=payload.email,
        encrypted_password=encrypt_password(payload.password),
        regexes=payload.regexes,
    )
    db.add(sweeper)
    await db.commit()

    return SweeperCreateResponse(success=True, message="email added successfully", email=payload.email)


@router.patch("/{email}", response_model=SweeperRead)
async def edit_sweepers(email: str, payload: SweeperRegexUpdateRequest, db: AsyncSession = Depends(get_db)):
    sweeper = await db.scalar(select(MailboxSweeper).where(MailboxSweeper.email == email))
    if not sweeper:
        raise HTTPException(status_code=404, detail="email not found")

    current = set(sweeper.regexes or [])
    current -= set(payload.remove_regexes)
    current |= set(payload.add_regexes)
    sweeper.regexes = list(current)

    await db.commit()
    await db.refresh(sweeper)
    return sweeper


@router.delete("/{email}", response_model=SweeperRemoveResponse)
async def remove_email(email: str, db: AsyncSession = Depends(get_db)):
    sweeper = await db.scalar(select(MailboxSweeper).where(MailboxSweeper.email == email))
    if not sweeper:
        raise HTTPException(status_code=404, detail="email not found")

    await db.delete(sweeper)
    await db.commit()
    return SweeperRemoveResponse(success=True, message="email removed")
