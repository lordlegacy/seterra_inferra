from pydantic import BaseModel
from enum import Enum

class StatusEnum(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketUpdate(BaseModel):
    status: StatusEnum

class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    user_id: int

    class Config:
        orm_mode = True
