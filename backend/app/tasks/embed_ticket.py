from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.models.ticket import Ticket
from backend.app.models.ticket_embedding import TicketEmbedding
from backend.app.llm.chunking import chunk_text
from backend.app.llm.embedding import embed_texts

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
