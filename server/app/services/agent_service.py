import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from uuid import UUID
from datetime import datetime
import json

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database_models import AgentTask, TaskStatusEnum
from app.models.api_models import AgentTaskCreate, AgentTaskStatus, TaskStatus
from app.agents.autogen_agents import run_agent_chat
from app.agents.langgraph_workflow import execute_workflow

logger = logging.getLogger(__name__)

async def create_agent_task(db: AsyncSession, task_request: AgentTaskCreate) -> AgentTask:
    """Create a new agent task in the database.
    
    Args:
        db: Database session
        task_request: Task creation request
        
    Returns:
        Created AgentTask object
    """
    # Create new task
    task = AgentTask(
        status=TaskStatusEnum.PENDING,
        initial_request=task_request.dict(),
        intermediate_steps={"step_count": 0, "total_steps": 0}
    )
    
    # Add to database
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    logger.info(f"Created task: {task.id}")
    
    return task

async def get_task_by_id(db: AsyncSession, task_id: UUID) -> Optional[AgentTask]:
    """Get a task by ID.
    
    Args:
        db: Database session
        task_id: Task ID
        
    Returns:
        AgentTask if found, None otherwise
    """
    result = await db.execute(select(AgentTask).where(AgentTask.id == task_id))
    return result.scalars().first()

async def get_task_status(db: AsyncSession, task_id: UUID) -> Optional[TaskStatus]:
    """Get task status.
    
    Args:
        db: Database session
        task_id: Task ID
        
    Returns:
        Task status enum value if task exists, None otherwise
    """
    task = await get_task_by_id(db, task_id)
    if task:
        return task.status
    return None

async def get_recent_tasks(db: AsyncSession, limit: int = 10, offset: int = 0) -> List[AgentTask]:
    """Get recent tasks with pagination.
    
    Args:
        db: Database session
        limit: Maximum number of tasks to return
        offset: Number of tasks to skip
        
    Returns:
        List of AgentTask objects
    """
    result = await db.execute(
        select(AgentTask)
        .order_by(desc(AgentTask.created_at))
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()

async def update_task_status(
    db: AsyncSession, 
    task_id: UUID, 
    status: TaskStatusEnum,
    intermediate_steps: Optional[Dict[str, Any]] = None,
    final_result: Optional[Dict[str, Any]] = None
) -> bool:
    """Update task status and optionally intermediate steps and final result.
    
    Args:
        db: Database session
        task_id: Task ID
        status: New task status
        intermediate_steps: Optional intermediate steps to update
        final_result: Optional final result to update
        
    Returns:
        True if task was updated, False otherwise
    """
    task = await get_task_by_id(db, task_id)
    if not task:
        return False
    
    # Update status
    task.status = status
    
    # Update timestamps based on status
    if status == TaskStatusEnum.RUNNING and not task.started_at:
        task.started_at = datetime.utcnow()
    elif status in [TaskStatusEnum.COMPLETED, TaskStatusEnum.FAILED] and not task.completed_at:
        task.completed_at = datetime.utcnow()
    
    # Update intermediate steps if provided
    if intermediate_steps is not None:
        task.intermediate_steps = intermediate_steps
    
    # Update final result if provided
    if final_result is not None:
        task.final_result = final_result
    
    # Update task in database
    await db.commit()
    await db.refresh(task)
    
    return True

async def run_agent_task(db: AsyncSession, task_id: UUID, task_request: AgentTaskCreate) -> Dict[str, Any]:
    """Run an agent task using either Autogen or LangGraph based on the task type.
    
    Args:
        db: Database session
        task_id: Task ID
        task_request: Task request data
        
    Returns:
        Dictionary with task execution results
    """
    logger.info(f"Running task {task_id}: {task_request.task_type}")
    
    try:
        # Update task status to running
        await update_task_status(db, task_id, TaskStatusEnum.RUNNING)
        
        task_type = task_request.task_type
        request_data = task_request.request_data
        
        # Choose execution mechanism based on task type
        if task_type in ["research", "strategy", "backtest"]:
            # Simple tasks can use Autogen directly
            results = await run_agent_chat({
                "task_type": task_type,
                "request_data": request_data
            })
            
            # Update task with final results
            if results.get("success", False):
                await update_task_status(
                    db, 
                    task_id,
                    TaskStatusEnum.COMPLETED,
                    intermediate_steps={"step_count": 1, "total_steps": 1, "current_step": "complete"},
                    final_result=results
                )
            else:
                await update_task_status(
                    db, 
                    task_id,
                    TaskStatusEnum.FAILED,
                    intermediate_steps={"step_count": 1, "total_steps": 1, "current_step": "failed"},
                    final_result={"error": results.get("error", "Unknown error")}
                )
                
        elif task_type == "end_to_end":
            # For complex workflows, use LangGraph
            # This is a streaming execution
            try:
                # Set up initial step count
                await update_task_status(
                    db, 
                    task_id,
                    TaskStatusEnum.RUNNING,
                    intermediate_steps={
                        "step_count": 0, 
                        "total_steps": 5,  # planning, research, strategy, backtest, finalization
                        "current_step": "initialization"
                    }
                )
                
                # Start the workflow - this may be a long-running task
                async for step_result in execute_workflow(task_id, {
                    "task_type": task_type,
                    "request_data": request_data
                }):
                    # Update task with intermediate steps
                    if not step_result.get("is_final", False):
                        await update_task_status(
                            db, 
                            task_id,
                            TaskStatusEnum.RUNNING,
                            intermediate_steps={
                                "step_count": step_result["step_count"],
                                "total_steps": 5,
                                "current_step": step_result["current_step"]
                            }
                        )
                    else:
                        # Final update with results
                        if "error" in step_result:
                            await update_task_status(
                                db, 
                                task_id,
                                TaskStatusEnum.FAILED,
                                intermediate_steps={
                                    "step_count": step_result.get("step_count", 0),
                                    "total_steps": 5,
                                    "current_step": "error"
                                },
                                final_result={"error": step_result["error"]}
                            )
                        else:
                            # Extract the final result from the state
                            final_state = step_result.get("state", {})
                            final_result = final_state.get("final_result", {})
                            
                            await update_task_status(
                                db, 
                                task_id,
                                TaskStatusEnum.COMPLETED,
                                intermediate_steps={
                                    "step_count": 5,
                                    "total_steps": 5,
                                    "current_step": "completed"
                                },
                                final_result=final_result
                            )
                
            except Exception as e:
                logger.error(f"Error in workflow execution: {e}", exc_info=True)
                await update_task_status(
                    db, 
                    task_id,
                    TaskStatusEnum.FAILED,
                    final_result={"error": str(e)}
                )
                
        else:
            # Unsupported task type
            await update_task_status(
                db, 
                task_id,
                TaskStatusEnum.FAILED,
                final_result={"error": f"Unsupported task type: {task_type}"}
            )
        
        # Get the final task state
        task = await get_task_by_id(db, task_id)
        if task:
            return {
                "task_id": task.id,
                "status": task.status,
                "final_result": task.final_result
            }
        else:
            return {"error": "Task not found after execution"}
        
    except Exception as e:
        logger.error(f"Error running task {task_id}: {e}", exc_info=True)
        
        # Update task status to failed
        await update_task_status(
            db, 
            task_id,
            TaskStatusEnum.FAILED,
            final_result={"error": str(e)}
        )
        
        return {"error": str(e)} 