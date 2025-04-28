from sqlalchemy import Column, Integer
from pgvector.sqlalchemy import Vector
from app.db import Base

class TicketEmbedding(Base):
    __tablename__ = "ticket_embeddings"

    ticket_id = Column(Integer, primary_key=True)
    embedding = Column(Vector(768))
