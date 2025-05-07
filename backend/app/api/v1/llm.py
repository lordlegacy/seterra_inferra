from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.deps import get_db, get_current_user
from backend.app.models.user import User
from backend.app.llm.llm_service import resolve_ticket

router = APIRouter()

@router.post("/resolve_ticket/{ticket_id}")
def resolve_ticket_route(
    ticket_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Optional: restrict to support/admin roles
    if user.role not in ("support", "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    result = resolve_ticket(ticket_id, db)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
