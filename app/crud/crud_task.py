from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskStatus, TaskType
from app.schemas.task import TaskCreate, TaskUpdate, TaskFilter

async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_task(db: AsyncSession, task_id: UUID) -> Optional[Task]:
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task_status(db: AsyncSession, task_id: UUID, status: TaskStatus, error_details: Optional[str] = None) -> Optional[Task]:
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    
    db_task.status = status
    if error_details:
        db_task.error_details = error_details
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task_plan(db: AsyncSession, task_id: UUID, plan: Dict[str, Any]) -> Optional[Task]:
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    
    db_task.plan = plan
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def list_tasks_filtered(
    db: AsyncSession,
    filter_params: TaskFilter,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:
    query = select(Task)
    
    if filter_params.task_types:
        query = query.filter(Task.task_type.in_(filter_params.task_types))
    if filter_params.statuses:
        query = query.filter(Task.status.in_(filter_params.statuses))
    if filter_params.start_date:
        query = query.filter(Task.created_at >= filter_params.start_date)
    if filter_params.end_date:
        query = query.filter(Task.created_at <= filter_params.end_date)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()