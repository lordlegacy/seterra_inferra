from sqlalchemy import Column, Integer, Text, DateTime
from pgvector.sqlalchemy import Vector
from backend.app.db import Base
from datetime import datetime

class WebSnippet(Base):
    __tablename__ = "web_snippets"

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    title = Column(Text)
    content = Column(Text)
    embedding = Column(Vector(768))
    retrieved_at = Column(DateTime, default=datetime.utcnow)
