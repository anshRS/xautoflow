from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel
from app.models.task import TaskType, TaskStatus

class TaskBase(BaseModel):
    task_type: TaskType
    input_data: Dict[str, Any]

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: UUID
    status: TaskStatus
    generated_plan: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PlanApproval(BaseModel):
    approved: bool
    modified_plan: Optional[Dict[str, Any]] = None