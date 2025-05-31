from sqlalchemy import Column, Integer, String
from app.database import Base
from app.models.enum import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default=UserRole.USER.value)  # Enumの値
    is_active = Column(Integer, default=1)
