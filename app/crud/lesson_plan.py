from sqlalchemy.orm import Session
from app.models.lesson_plan import LessonPlan
from app.schemas.lesson_plan import LessonPlanCreate
from typing import List, Optional

def create_lesson_plan(db: Session, data: LessonPlanCreate) -> LessonPlan:
    plan = LessonPlan(**data.dict())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

def get_lesson_plan(db: Session, id: str) -> Optional[LessonPlan]:
    return db.query(LessonPlan).filter(LessonPlan.id == id).first()

def list_lesson_plans(db: Session) -> List[LessonPlan]:
    return db.query(LessonPlan).filter(LessonPlan.parent_id == None).all()

def archive_lesson_plan(db: Session, id: str) -> Optional[LessonPlan]:
    plan = db.query(LessonPlan).filter(LessonPlan.id == id).first()
    if plan:
        plan.is_archived = True
        db.commit()
        db.refresh(plan)
    return plan

def unarchive_lesson_plan(db: Session, id: str) -> Optional[LessonPlan]:
    plan = db.query(LessonPlan).filter(LessonPlan.id == id).first()
    if plan:
        plan.is_archived = False
        db.commit()
        db.refresh(plan)
    return plan

def get_children(db: Session, parent_id: str) -> List[LessonPlan]:
    return db.query(LessonPlan).filter(LessonPlan.parent_id == parent_id).all()

def fork_lesson_plan(db: Session, original_id: str) -> Optional[LessonPlan]:
    base = get_lesson_plan(db, original_id)
    if not base:
        return None
    cloned = LessonPlan(
        title=f"{base.title} の分岐",
        content=base.content,
        subject=base.subject,
        grade=base.grade,
        goal=base.goal,
        parent_id=base.id,
        is_archived=False  # 初期状態で有効
    )
    db.add(cloned)
    db.commit()
    db.refresh(cloned)
    return cloned

