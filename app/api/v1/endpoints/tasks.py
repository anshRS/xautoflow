from typing import List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskSchema, PlanApproval, TaskFilter, TaskList
from app.models.task import TaskStatus, TaskType
from app.crud import crud_task
from app.core.security import verify_api_key
from app.services.task_service import TaskService

router = APIRouter()

@router.post("/", response_model=TaskSchema)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    service = TaskService(db)
    task_id = await service.start_task(task)
    return await crud_task.get_task(db, task_id)

@router.put("/{task_id}/approve", response_model=TaskSchema)
async def approve_task_plan(
    task_id: UUID,
    approval: PlanApproval,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    service = TaskService(db)
    await service.approve_task_plan(task_id, approval)
    return await crud_task.get_task(db, task_id)

@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    task = await crud_task.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=TaskList)
async def list_tasks(
    task_types: List[TaskType] = Query(None),
    statuses: List[TaskStatus] = Query(None),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    filter_params = TaskFilter(
        task_types=task_types,
        statuses=statuses,
        start_date=start_date,
        end_date=end_date
    )
    tasks = await crud_task.list_tasks_filtered(db, filter_params, skip, limit)
    total = len(tasks)  # In a real app, you'd want to do a separate count query
    return TaskList(items=tasks, total=total)