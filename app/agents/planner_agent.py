from typing import Dict, Any
from app.agents.base_agent import BaseAssistantAgent, get_base_llm_config

PLANNER_PROMPT = """You are a workflow planning agent responsible for creating detailed execution plans.
Your task is to break down complex workflows into clear, actionable steps.
Consider dependencies, resources, and potential bottlenecks in your planning.
Always ensure your plans are practical and executable."""

class PlannerAgent(BaseAssistantAgent):
    def __init__(self):
        super().__init__(
            name="planner",
            description="Workflow planning and task breakdown specialist",
            llm_config=get_base_llm_config()
        )
        self.system_prompt = PLANNER_PROMPT

    async def generate_plan(self, task_type: str, initial_request: str) -> Dict[str, Any]:
        """Generate a workflow plan based on the task type and initial request."""
        prompt = f"""Task Type: {task_type}
Initial Request: {initial_request}

Please create a detailed workflow plan that includes:
1. Main objectives
2. Required steps
3. Dependencies between steps
4. Estimated timeframes
5. Required resources
6. Potential risks and mitigation strategies

Format the response as a structured JSON with these sections."""

        response = await self.generate_response(prompt)
        # TODO: Add JSON parsing and validation
        return {"plan": response, "status": "success"}

def create_planner_agent() -> PlannerAgent:
    return PlannerAgent()