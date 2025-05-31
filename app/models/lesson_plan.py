from sqlalchemy import Column, String, Text, DateTime
from uuid import uuid4
from datetime import datetime
from app.db.database import Base

class LessonPlan(Base):
    __tablename__ = "lesson_plans"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    evaluation = Column(Text, nullable=False)
    memo = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
