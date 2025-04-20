from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum

# --- Auth Models ---

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str  # User ID as subject
    exp: Optional[int] = None  # Expiration time

# --- Agent Task Models ---

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# --- Agent-specific request/response models ---

class MarketResearchRequest(BaseModel):
    ticker_symbol: str
    time_horizon: str = Field(..., description="e.g., 'short_term', 'long_term'")
    research_depth: str = Field(..., description="e.g., 'basic', 'comprehensive'")
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to research: fundamentals, technicals, news, sentiment")
    additional_context: Optional[str] = None

class StrategyDevRequest(BaseModel):
    ticker_symbol: str
    time_horizon: str
    strategy_type: str = Field(..., description="e.g., 'trend_following', 'mean_reversion', 'breakout', 'custom'")
    risk_profile: str = Field(..., description="e.g., 'conservative', 'moderate', 'aggressive'")
    include_indicators: Optional[List[str]] = None
    custom_requirements: Optional[str] = None
    research_results: Optional[Dict[str, Any]] = None  # Can include previous research results

class BacktestRequest(BaseModel):
    strategy_id: Optional[UUID] = None
    strategy_code: Optional[str] = None  # Alternative to strategy_id if testing a new strategy directly
    strategy_params: Optional[Dict[str, Any]] = None
    ticker_symbol: str
    start_date: datetime
    end_date: datetime
    initial_capital: float = 10000.0
    additional_settings: Optional[Dict[str, Any]] = None

class BacktestResult(BaseModel):
    id: UUID
    strategy_id: UUID
    start_date: datetime
    end_date: datetime
    total_return: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    win_rate: Optional[float] = None
    metrics: Dict[str, Any]
    equity_curve: Optional[Dict[str, List[float]]] = None
    trades: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Strategy(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]
    code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- LangGraph Workflow Models ---

class WorkflowStateUpdate(BaseModel):
    """Model for updates from LangGraph state during workflow processing."""
    task_id: UUID
    current_node: str
    step_number: int
    state_data: Dict[str, Any]
    log_message: Optional[str] = None
    is_complete: bool = False

# --- Complete Workflow Request Models ---

class AgentTaskCreate(BaseModel):
    """Generic request model for creating a new agent task.
    The request_data will contain the specific payload needed for the task type.
    """
    task_type: str = Field(..., description="Type of task: 'research', 'strategy', 'backtest', 'end_to_end'")
    request_data: Dict[str, Any] = Field(..., description="Task-specific data structure")

class AgentTaskResponse(BaseModel):
    """Response model for agent task creation."""
    task_id: UUID
    status: TaskStatus
    created_at: datetime
    message: str = "Task created successfully. Check status for updates."

class AgentTaskStatus(BaseModel):
    """Status check response model for agent tasks."""
    task_id: UUID
    status: TaskStatus
    progress: Optional[float] = None  # 0.0 to 1.0
    current_step: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_summary: Optional[Dict[str, Any]] = None

class EndToEndWorkflowRequest(BaseModel):
    """Request model for a complete end-to-end workflow: research > strategy > backtest."""
    ticker_symbol: str
    time_horizon: str
    risk_profile: str
    strategy_type: Optional[str] = None
    custom_requirements: Optional[str] = None
    backtest_start_date: Optional[datetime] = None
    backtest_end_date: Optional[datetime] = None
    additional_context: Optional[str] = None

# --- Llamaindex/RAG Models ---

class KnowledgeBaseQuery(BaseModel):
    """Model for querying the knowledge base."""
    query: str
    top_k: int = 5
    filter_metadata: Optional[Dict[str, Any]] = None

class DocumentChunk(BaseModel):
    """Model for a document chunk returned from the knowledge base."""
    text: str
    metadata: Dict[str, Any]
    score: Optional[float] = None

class KnowledgeBaseResponse(BaseModel):
    """Response model for knowledge base queries."""
    query: str
    results: List[DocumentChunk]
    total_results: int

class DocumentUpload(BaseModel):
    """Model for document upload response."""
    filename: str
    success: bool
    document_id: Optional[UUID] = None
    message: Optional[str] = None 