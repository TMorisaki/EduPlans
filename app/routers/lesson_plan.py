from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.lesson_plan import LessonPlanCreate, LessonPlanRead
from app.db.database import SessionLocal
from app.crud import lesson_plan as crud

router = APIRouter(prefix="/lesson-plans", tags=["Lesson Plans"])

# DBセッション依存解決関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=LessonPlanRead)
def create(plan: LessonPlanCreate, db: Session = Depends(get_db)):
    return crud.create_lesson_plan(db, plan)

@router.get("", response_model=List[LessonPlanRead])
def list_all(db: Session = Depends(get_db)):
    return crud.get_lesson_plans(db)

@router.get("/{lesson_id}", response_model=LessonPlanRead)
def get(lesson_id: str, db: Session = Depends(get_db)):
    plan = crud.get_lesson_plan(db, lesson_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Lesson plan not found")
    return plan
