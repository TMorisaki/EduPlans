from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.lesson_plan import LessonPlanCreate, LessonPlanResponse
from app.crud import lesson_plan as crud

router = APIRouter(prefix="/lesson-plans", tags=["Lesson Plans"])

@router.post("", response_model=LessonPlanResponse)
def create(plan: LessonPlanCreate, db: Session = Depends(get_db)):
    return crud.create_lesson_plan(db, plan)

@router.get("/{lesson_plan_id}", response_model=LessonPlanResponse)
def get(lesson_plan_id: str, db: Session = Depends(get_db)):
    plan = crud.get_lesson_plan(db, lesson_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Lesson plan not found")
    return plan

@router.get("", response_model=List[LessonPlanResponse])
def list_all(db: Session = Depends(get_db)):
    return crud.list_lesson_plans(db)

@router.patch("/{lesson_plan_id}/archive", response_model=LessonPlanResponse)
def archive(lesson_plan_id: str, db: Session = Depends(get_db)):
    plan = crud.archive_lesson_plan(db, lesson_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Lesson plan not found")
    return plan

@router.patch("/{lesson_plan_id}/unarchive", response_model=LessonPlanResponse)
def unarchive(lesson_plan_id: str, db: Session = Depends(get_db)):
    plan = crud.unarchive_lesson_plan(db, lesson_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Lesson plan not found")
    return plan

@router.get("/{lesson_plan_id}/children", response_model=List[LessonPlanResponse])
def children(lesson_plan_id: str, db: Session = Depends(get_db)):
    children = crud.get_children(db, lesson_plan_id)
    return children

@router.post("/{lesson_plan_id}/fork", response_model=LessonPlanResponse)
def fork(lesson_plan_id: str, db: Session = Depends(get_db)):
    plan = crud.fork_lesson_plan(db, lesson_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Lesson plan not found")
    return plan
