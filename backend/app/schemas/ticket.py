from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

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


from typing import List, Optional

class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    user_id: int
    solution: Optional[List[str]] = None 

    class Config:
        orm_mode = True

