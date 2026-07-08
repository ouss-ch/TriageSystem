"""Pydantic schemas for Ticket read/list."""

import datetime

from pydantic import BaseModel


class TicketRead(BaseModel):
    id: int
    mailbox_sweeper_id: int
    message_id: str
    sender: str
    subject: str
    body: str
    received_at: datetime.datetime
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


class TicketList(BaseModel):
    total: int
    items: list[TicketRead]
