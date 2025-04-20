from enum import Enum as PyEnum
import uuid
from sqlalchemy import Column, String, JSON, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from app.db.session import Base

class TaskType(str, PyEnum):
    RESEARCH = "RESEARCH"
    STRATEGY_DEV = "STRATEGY_DEV"
    BACKTEST = "BACKTEST"

class TaskStatus(str, PyEnum):
    PLANNING = "PLANNING"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_type = Column(Enum(TaskType), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PLANNING)
    input_data = Column(JSONB, nullable=False)
    generated_plan = Column(JSONB)
    result = Column(JSONB)
    metadata = Column(JSONB, default={})
    
    __table_args__ = (
        Index('idx_task_type_status', 'task_type', 'status'),
        Index('idx_created_at', 'created_at'),
    )
    error_details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)