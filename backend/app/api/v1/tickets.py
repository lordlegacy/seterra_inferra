from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from backend.app.services.ticket_service import *
from backend.app.core.deps import get_current_user, get_db
from backend.app.models.user import User
from backend.app.services.ticket_service import create_ticket
from backend.app.core.logger import logger

router = APIRouter()

@router.post("/", response_model=TicketOut)
def create_ticket_route(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ticket = create_ticket(
        db,
        user_id=user.id,
        title=ticket_data.title,
        description=ticket_data.description
    )
    return ticket



@router.get("/", response_model=list[TicketOut])
def list_user_tickets(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role in ["support", "admin"]:
        return get_all_tickets(db)
    return get_user_tickets(db, user.id)

@router.patch("/{ticket_id}", response_model=TicketOut)
def update_status(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role not in ["support", "admin"]:
        raise HTTPException(status_code=403)
    return update_ticket_status(db, ticket_id, payload.status)

