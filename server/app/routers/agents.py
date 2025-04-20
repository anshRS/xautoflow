from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.database import get_db
from app.models.api_models import (
    AgentTaskCreate, 
    AgentTaskResponse, 
    AgentTaskStatus,
    EndToEndWorkflowRequest
)
from app.models.database_models import AgentTask, TaskStatusEnum
from app.services.agent_service import (
    create_agent_task,
    get_task_status,
    get_task_by_id,
    get_recent_tasks,
    run_agent_task
)

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/tasks", response_model=AgentTaskResponse)
async def create_task(
    task_request: AgentTaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> AgentTaskResponse:
    """Create a new agent task to be executed asynchronously."""
    task = await create_agent_task(db, task_request)
    
    # Schedule the task to run in the background
    background_tasks.add_task(run_agent_task, db, task.id, task_request)
    
    return AgentTaskResponse(
        task_id=task.id,
        status=task.status,
        created_at=task.created_at,
        message="Task created successfully. Check status endpoint for updates."
    )

@router.get("/tasks/{task_id}", response_model=AgentTaskStatus)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> AgentTaskStatus:
    """Get the status and results of a specific task."""
    task = await get_task_by_id(db, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Calculate progress as a float between 0 and 1
    progress = None
    if task.status == TaskStatusEnum.RUNNING and task.intermediate_steps:
        # Extract progress information from intermediate_steps if available
        steps = task.intermediate_steps
        if isinstance(steps, dict) and "step_count" in steps and "total_steps" in steps:
            progress = min(1.0, steps["step_count"] / steps["total_steps"])
    
    # Get current step name if available
    current_step = None
    if task.intermediate_steps and isinstance(task.intermediate_steps, dict):
        current_step = task.intermediate_steps.get("current_step")
    
    return AgentTaskStatus(
        task_id=task.id,
        status=task.status,
        progress=progress,
        current_step=current_step,
        created_at=task.created_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        result_summary=task.final_result
    )

@router.get("/tasks", response_model=List[AgentTaskStatus])
async def list_tasks(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
) -> List[AgentTaskStatus]:
    """List recent agent tasks."""
    tasks = await get_recent_tasks(db, limit, offset)
    
    result = []
    for task in tasks:
        # Calculate progress
        progress = None
        if task.status == TaskStatusEnum.RUNNING and task.intermediate_steps:
            steps = task.intermediate_steps
            if isinstance(steps, dict) and "step_count" in steps and "total_steps" in steps:
                progress = min(1.0, steps["step_count"] / steps["total_steps"])
        
        # Get current step name if available
        current_step = None
        if task.intermediate_steps and isinstance(task.intermediate_steps, dict):
            current_step = task.intermediate_steps.get("current_step")
        
        result.append(AgentTaskStatus(
            task_id=task.id,
            status=task.status,
            progress=progress,
            current_step=current_step,
            created_at=task.created_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            result_summary=task.final_result
        ))
    
    return result

@router.post("/workflows/end-to-end", response_model=AgentTaskResponse)
async def create_end_to_end_workflow(
    workflow_request: EndToEndWorkflowRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> AgentTaskResponse:
    """Create an end-to-end workflow that conducts research, develops a strategy, and backtest."""
    # Convert EndToEndWorkflowRequest to AgentTaskCreate
    task_request = AgentTaskCreate(
        task_type="end_to_end",
        request_data={
            "ticker_symbol": workflow_request.ticker_symbol,
            "time_horizon": workflow_request.time_horizon,
            "risk_profile": workflow_request.risk_profile,
            "strategy_type": workflow_request.strategy_type,
            "custom_requirements": workflow_request.custom_requirements,
            "backtest_start_date": workflow_request.backtest_start_date.isoformat() if workflow_request.backtest_start_date else None,
            "backtest_end_date": workflow_request.backtest_end_date.isoformat() if workflow_request.backtest_end_date else None,
            "additional_context": workflow_request.additional_context
        }
    )
    
    # Create and run the task
    task = await create_agent_task(db, task_request)
    background_tasks.add_task(run_agent_task, db, task.id, task_request)
    
    return AgentTaskResponse(
        task_id=task.id,
        status=task.status,
        created_at=task.created_at,
        message="End-to-end workflow created. This may take some time to complete."
    ) 