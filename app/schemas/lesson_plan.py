from pydantic import BaseModel
from datetime import datetime

class LessonPlanCreate(BaseModel):
    title: str
    grade: str
    subject: str
    unit: str
    content: str
    evaluation: str
    memo: str

class LessonPlanRead(LessonPlanCreate):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
