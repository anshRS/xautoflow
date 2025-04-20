import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.data.database import Base

class TaskStatusEnum(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship("AgentTask", back_populates="owner")

class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(SQLEnum(TaskStatusEnum), default=TaskStatusEnum.PENDING, nullable=False)
    initial_request = Column(JSON) # Store the original request
    final_result = Column(JSON, nullable=True) # Store the final output/result
    intermediate_steps = Column(JSON, nullable=True) # Store LangGraph state or key steps
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="tasks")
    strategy = relationship("Strategy", back_populates="task", uselist=False)
    backtest_result = relationship("BacktestResult", back_populates="task", uselist=False)

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("agent_tasks.id"))
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    parameters = Column(JSON) # e.g., indicator periods, thresholds
    code = Column(Text, nullable=True) # Optional: Store generated strategy code
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    task = relationship("AgentTask", back_populates="strategy")
    backtest_results = relationship("BacktestResult", back_populates="strategy") # A strategy might be backtested multiple times

class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("agent_tasks.id"), nullable=True) # Link to the task that ran the backtest
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=False) # Link to the strategy tested
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    total_return = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)
    metrics = Column(JSON) # Store all other metrics from vectorbt/backtrader
    equity_curve = Column(JSON, nullable=True) # Store equity curve data points
    trades = Column(JSON, nullable=True) # Store trade log
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("AgentTask", back_populates="backtest_result")
    strategy = relationship("Strategy", back_populates="backtest_results")

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=True, nullable=False)
    filepath = Column(String, unique=True, nullable=False) # Relative path within DOCUMENTS_DIR
    doc_id_llamaindex = Column(String, unique=True, nullable=True) # Store LlamaIndex internal doc ID
    metadata = Column(JSON, nullable=True) # Any extracted metadata
    indexed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 