from sqlalchemy.orm import Session
from app.models.ticket import Ticket, TicketStatus

def create_ticket(db: Session, title: str, description: str, user_id: int):
    ticket = Ticket(title=title, description=description, user_id=user_id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

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
