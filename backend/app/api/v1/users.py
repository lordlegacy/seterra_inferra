from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.models.user import User, UserRole
from backend.app.schemas.user import UserOut, RoleUpdate
from backend.app.core.deps import get_db, get_current_user

router = APIRouter()

# Admin-only decorator
def admin_required(user: User):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    admin_required(current_user)
    return db.query(User).all()

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/{user_id}/role", response_model=UserOut)
def update_user_role(user_id: int, role: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    admin_required(current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role.role
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    admin_required(current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": f"User {user.username} deleted"}
