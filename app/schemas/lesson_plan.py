from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LessonPlanCreate(BaseModel):
    title: str
    content: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    goal: Optional[str] = None
    parent_id: Optional[str] = None

class LessonPlanUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    goal: Optional[str] = None
    parent_id: Optional[str] = None
    is_archived: Optional[bool] = None

class LessonPlanResponse(BaseModel):
    id: str
    title: str
    content: Optional[str]
    subject: Optional[str]
    grade: Optional[str]
    goal: Optional[str]
    parent_id: Optional[str]
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
