from sqlalchemy import Column, Integer, String, Boolean, Enum
from backend.app.db import Base
import enum

class UserRole(str, enum.Enum):
    user = "user"
    support = "support"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.user)

