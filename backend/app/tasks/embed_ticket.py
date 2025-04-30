from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ticket import Ticket
from app.models.ticket_embedding import TicketEmbedding
from app.llm.chunking import chunk_text
from app.llm.embedding import embed_texts

def embed_all_tickets():
    db: Session = SessionLocal()
    tickets = db.query(Ticket).all()
    for ticket in tickets:
        chunks = chunk_text(ticket.description)
        embeddings = embed_texts(chunks)
        for chunk, vector in zip(chunks, embeddings):
            record = TicketEmbedding(
                ticket_id=ticket.id,
                chunk=chunk,
                embedding=vector
            )
            db.add(record)
    db.commit()
    db.close()

if __name__ == "__main__":
    embed_all_tickets()
