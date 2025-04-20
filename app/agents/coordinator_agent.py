from typing import Dict, Any, List
from autogen import UserProxyAgent, AssistantAgent
from .base_agent import get_base_llm_config
from app.tools.knowledge_tools import query_local_kb
from app.tools.news_api_tool import get_financial_news
from app.tools.financial_tools import (
    calculate_technical_indicators,
    fetch_historical_data,
    optimize_strategy_parameters
)
from app.agents.base_agent import BaseAssistantAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.executor_agent import ExecutorAgent

COORDINATOR_PROMPT = """You are a workflow coordinator responsible for managing the execution of complex tasks.
Your role is to:
1. Understand user requests and delegate to appropriate agents
2. Coordinate between planner and executor agents
3. Monitor progress and handle any issues
4. Ensure tasks are completed successfully
5. Provide clear status updates and results

Always maintain a clear overview of the workflow and ensure proper communication between agents."""

class CoordinatorAgent(BaseAssistantAgent):
    def __init__(self):
        super().__init__(
            name="coordinator",
            description="Workflow coordination and task management specialist",
            llm_config=get_base_llm_config()
        )
        self.system_prompt = COORDINATOR_PROMPT
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.current_workflow = None
        self.workflow_history = []

    async def handle_request(self, request: str) -> Dict[str, Any]:
        """Handle a new user request by coordinating the workflow."""
        # Generate plan using planner agent
        plan = await this.planner.generate_plan(request)
        
        # Initialize workflow
        this.current_workflow = {
            "request": request,
            "plan": plan,
            "status": "in_progress",
            "tasks": []
        }
        
        # Execute tasks using executor agent
        for task in plan.get("tasks", []):
            result = await this.executor.execute_task(task)
            this.current_workflow["tasks"].append(result)
            
            # Check for issues
            if result.get("status") != "success":
                this.current_workflow["status"] = "failed"
                break
        
        # Update workflow status
        if this.current_workflow["status"] != "failed":
            this.current_workflow["status"] = "completed"
        
        # Store in history
        this.workflow_history.append(this.current_workflow)
        
        return {
            "status": this.current_workflow["status"],
            "workflow": this.current_workflow
        }

    async def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Retrieve the history of completed workflows."""
        return this.workflow_history

def create_coordinator_agent() -> CoordinatorAgent:
    return CoordinatorAgent()