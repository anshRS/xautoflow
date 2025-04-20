from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate
from app.schemas.task import TaskFilter

def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(
        task_type=task.task_type,
        input_data=task.input_data,
        status=TaskStatus.PLANNING
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: UUID) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_status(db: Session, task_id: UUID, status: TaskStatus) -> Optional[Task]:
    task = get_task(db, task_id)
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task

def update_task_plan(db: Session, task_id: UUID, plan: dict) -> Optional[Task]:
    task = get_task(db, task_id)
    if task:
        task.generated_plan = plan
        task.status = TaskStatus.PENDING_APPROVAL
        db.commit()
        db.refresh(task)
    return task

def list_tasks_filtered(
    db: Session,
    filter_params: TaskFilter,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:
    query = db.query(Task)
    
    if filter_params.task_types:
        query = query.filter(Task.task_type.in_(filter_params.task_types))
    
    if filter_params.statuses:
        query = query.filter(Task.status.in_(filter_params.statuses))
    
    if filter_params.start_date:
        query = query.filter(Task.created_at >= filter_params.start_date)
    
    if filter_params.end_date:
        query = query.filter(Task.created_at <= filter_params.end_date)
    
    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()