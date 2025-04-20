from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, PlanApproval
from app.models.task import TaskStatus
from app.crud import crud_task

router = APIRouter()

@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    task_id = await service.start_task(task)
    return crud_task.get_task(db, task_id)

@router.put("/{task_id}/approve", response_model=TaskRead)
async def approve_task_plan(
    task_id: UUID,
    approval: PlanApproval,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    await service.approve_task_plan(task_id, approval)
    return crud_task.get_task(db, task_id)

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db)
):
    task = crud_task.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

from fastapi import Depends, Query
from app.core.security import verify_api_key

@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    task_types: List[TaskType] = Query(None),
    statuses: List[TaskStatus] = Query(None),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    filter_params = TaskFilter(
        task_types=task_types,
        statuses=statuses,
        start_date=start_date,
        end_date=end_date
    )
    return crud_task.list_tasks_filtered(db, filter_params, skip, limit)

@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    return await TaskService(db).start_task(task)