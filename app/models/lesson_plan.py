from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

class LessonPlan(Base):
    __tablename__ = "lesson_plans"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text)
    subject = Column(String)
    grade = Column(String)
    goal = Column(Text)
    parent_id = Column(String, ForeignKey("lesson_plans.id"), nullable=True)
    is_archived = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    children = relationship("LessonPlan", backref="parent", remote_side=[id])
