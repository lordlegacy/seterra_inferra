from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from backend.app.db import Base

import enum

class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(Enum(TicketStatus), default=TicketStatus.open)
    user_id = Column(Integer, ForeignKey("users.id"))
    solution = Column(Text, nullable=True)  # 👈 NEW

    user = relationship("User", backref="tickets")

