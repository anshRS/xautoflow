from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.task import TaskType, TaskStatus

class TaskBase(BaseModel):
    task_type: TaskType
    title: str
    description: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    task_type: Optional[TaskType] = None
    title: Optional[str] = None
    description: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    plan: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    status: Optional[TaskStatus] = None
    error_details: Optional[str] = None

class TaskSchema(TaskBase):
    id: UUID
    status: TaskStatus
    plan: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskList(BaseModel):
    items: list[TaskSchema]
    total: int

class PlanApproval(BaseModel):
    approved: bool
    modified_plan: Optional[Dict[str, Any]] = None

class TaskFilter(BaseModel):
    task_types: Optional[List[TaskType]] = None
    statuses: Optional[List[TaskStatus]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None