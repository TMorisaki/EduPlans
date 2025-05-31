from sqlalchemy.orm import Session
from app.models.lesson_plan import LessonPlan
from app.schemas.lesson_plan import LessonPlanCreate

def create_lesson_plan(db: Session, data: LessonPlanCreate) -> LessonPlan:
    plan = LessonPlan(**data.dict())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

def get_lesson_plans(db: Session):
    return db.query(LessonPlan).all()

def get_lesson_plan(db: Session, lesson_id: str):
    return db.query(LessonPlan).filter(LessonPlan.id == lesson_id).first()
