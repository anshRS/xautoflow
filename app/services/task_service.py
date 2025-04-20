from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_task
from app.models.task import TaskStatus, TaskType
from app.schemas.task import TaskCreate, PlanApproval
from app.workflows.research_workflow import ResearchWorkflow
from app.workflows.strategy_workflow import StrategyWorkflow
from app.workflows.backtest_workflow import BacktestWorkflow
from app.workflows.state import WorkflowState

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    async def start_task(self, task_create: TaskCreate) -> UUID:
        # Create task in DB
        task = crud_task.create_task(self.db, task_create)
        
        # Initialize workflow state
        initial_state = WorkflowState(
            task_id=task.id,
            task_type=task_create.task_type,
            initial_request=task_create.input_data,
            plan_approved=False,
            agent_inputs={},
            agent_outputs={},
            intermediate_results={},
            current_plan=None,
            final_result=None,
            error_info=None,
            metadata={}
        )

        # Start workflow based on task type
        try:
            if task_create.task_type == TaskType.RESEARCH:
                workflow = ResearchWorkflow(task.id, self.db)
            elif task_create.task_type == TaskType.STRATEGY_DEV:
                workflow = StrategyWorkflow(task.id, self.db)
            elif task_create.task_type == TaskType.BACKTEST:
                workflow = BacktestWorkflow(task.id, self.db)
            else:
                raise ValueError(f"Unsupported task type: {task_create.task_type}")
            
            await workflow.execute(initial_state)
        except Exception as e:
            crud_task.update_task_status(
                self.db,
                task.id,
                TaskStatus.FAILED,
                error_details=str(e)
            )
            raise HTTPException(500, f"Workflow execution failed: {str(e)}")
        
        return task.id

    async def approve_task_plan(
        self,
        task_id: UUID,
        approval: PlanApproval
    ) -> None:
        task = crud_task.get_task(self.db, task_id)
        if not task:
            raise HTTPException(404, "Task not found")
            
        if task.status != TaskStatus.PENDING_APPROVAL:
            raise HTTPException(400, "Task is not pending approval")

        if approval.approved:
            if approval.modified_plan:
                crud_task.update_task_plan(
                    self.db,
                    task_id,
                    approval.modified_plan
                )
            crud_task.update_task_status(
                self.db,
                task_id,
                TaskStatus.RUNNING
            )
            
            # Resume workflow execution
            try:
                workflow = self._get_workflow_for_task(task)
                state = WorkflowState(
                    task_id=task.id,
                    task_type=task.task_type,
                    initial_request=task.input_data,
                    current_plan=task.generated_plan,
                    plan_approved=True,
                    agent_inputs={},
                    agent_outputs={},
                    intermediate_results={},
                    final_result=None,
                    error_info=None,
                    metadata={}
                )
                await workflow.execute(state)
            except Exception as e:
                crud_task.update_task_status(
                    self.db,
                    task_id,
                    TaskStatus.FAILED,
                    error_details=str(e)
                )
                raise HTTPException(500, f"Workflow execution failed: {str(e)}")
        else:
            crud_task.update_task_status(
                self.db,
                task_id,
                TaskStatus.PLANNING
            )
    
    def _get_workflow_for_task(self, task):
        """Get the appropriate workflow instance for a task."""
        if task.task_type == TaskType.RESEARCH:
            return ResearchWorkflow(task.id, self.db)
        elif task.task_type == TaskType.STRATEGY_DEV:
            return StrategyWorkflow(task.id, self.db)
        elif task.task_type == TaskType.BACKTEST:
            return BacktestWorkflow(task.id, self.db)
        else:
            raise ValueError(f"Unsupported task type: {task.task_type}")