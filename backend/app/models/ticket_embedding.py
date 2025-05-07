from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey
from backend.app.db import Base


class TicketEmbedding(Base):
    __tablename__ = "ticket_embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), index=True)
    chunk = Column(Text)
    embedding = Column(Vector(768))

