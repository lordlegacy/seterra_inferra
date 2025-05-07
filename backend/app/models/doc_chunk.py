from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector 
from backend.app.db import Base


class DocChunk(Base):
    __tablename__ = "doc_chunks"

    id = Column(Integer, primary_key=True)
    source = Column(Text)
    chunk = Column(Text)
    embedding = Column(Vector(768))

