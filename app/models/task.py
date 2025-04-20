from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, DateTime, Enum as SQLEnum, JSON, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.models.base import Base

class TaskType(str, Enum):
    RESEARCH = "RESEARCH"
    STRATEGY_DEV = "STRATEGY_DEV"
    BACKTEST = "BACKTEST"

class TaskStatus(str, Enum):
    PLANNING = "planning"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}

    id = Column(PGUUID, primary_key=True, default=uuid4)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True)
    task_type = Column(SQLEnum(TaskType), nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PLANNING)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    input_data = Column(JSON, nullable=True)
    plan = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_details = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    workflow = relationship("Workflow", back_populates="tasks")