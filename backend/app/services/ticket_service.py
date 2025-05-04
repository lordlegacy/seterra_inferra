from app.models.ticket import Ticket, TicketStatus
from app.models.ticket_embedding import TicketEmbedding
from app.llm.chunking import chunk_text
from app.llm.embedding import embed_texts
from app.llm.llm_service import resolve_ticket  # this runs RAG + LLM
from sqlalchemy.orm import Session
from app.core.logger import logger



def get_user_tickets(db: Session, user_id: int):
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def update_ticket_status(db: Session, ticket_id: int, new_status: TicketStatus):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket:
        ticket.status = new_status
        db.commit()
        db.refresh(ticket)
    return ticket



def create_ticket(db: Session, user_id: int, title: str, description: str) -> Ticket:
    # Step 1: Create ticket object
    new_ticket = Ticket(
        title=title,
        description=description,
        user_id=user_id
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    logger.info("Ticket created")

# Step 2: Run LLM-based resolution and store the solution
    result = resolve_ticket(new_ticket.id, db)
    if isinstance(result, dict) and "solutions" in result:
        new_ticket.solution = "\n".join(result["solutions"])
        db.commit()
        db.refresh(new_ticket)
        logger.info("LLM solution")

    # Step 3: Re-embed the ticket with full content (desc + solution)
    full_text = f"{new_ticket.title}\n{new_ticket.description}\n{new_ticket.solution or ''}"
    db.query(TicketEmbedding).filter(TicketEmbedding.ticket_id == new_ticket.id).delete()

    chunks = chunk_text(full_text)
    vectors = embed_texts(chunks)

    for chunk, vector in zip(chunks, vectors):
        db.add(TicketEmbedding(
            ticket_id=new_ticket.id,
            chunk=chunk,
            embedding=vector
        ))

    db.commit()
    logger.info("Re-embedding")
    return new_ticket
