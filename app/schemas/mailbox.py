"""Pydantic schemas for mailbox sweeper registration (add/edit/remove)."""

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class SweeperCreateRequest(BaseModel):
    email: EmailStr
    password: str
    regexes: List[str] = Field(default_factory=list)


class SweeperCreateResponse(BaseModel):
    success: bool
    message: str
    email: Optional[EmailStr] = None


class SweeperRegexUpdateRequest(BaseModel):
    add_regexes: List[str] = Field(default_factory=list)
    remove_regexes: List[str] = Field(default_factory=list)


class SweeperRead(BaseModel):
    email: EmailStr
    regexes: List[str]

    model_config = {"from_attributes": True}


class SweeperRemoveResponse(BaseModel):
    success: bool
    message: str
