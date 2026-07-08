"""Ticket endpoints — list/get raw ingested support tickets."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketList, TicketRead

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=TicketList)
async def list_tickets(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count()).select_from(Ticket))
    rows = await db.scalars(
        select(Ticket).order_by(Ticket.received_at.desc()).offset(skip).limit(limit)
    )
    return TicketList(total=total, items=list(rows))


@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket not found")
    return ticket
