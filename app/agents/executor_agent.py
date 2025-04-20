from typing import Dict, Any, List
from app.agents.base_agent import BaseAssistantAgent, get_base_llm_config

EXECUTOR_PROMPT = """You are a task execution agent responsible for carrying out specific steps in a workflow.
Your role is to execute tasks precisely according to the plan, while adapting to any challenges that arise.
Always report your progress and any issues encountered during execution."""

class ExecutorAgent(BaseAssistantAgent):
    def __init__(self):
        super().__init__(
            name="executor",
            description="Task execution and workflow step implementation specialist",
            llm_config=get_base_llm_config()
        )
        self.system_prompt = EXECUTOR_PROMPT
        self.current_task = None
        self.task_history = []

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task from the workflow plan."""
        self.current_task = task
        prompt = f"""Task Details:
{task}

Please execute this task and provide:
1. Status of execution
2. Results or output
3. Any issues encountered
4. Recommendations for next steps

Format the response as a structured JSON."""

        response = await this.generate_response(prompt)
        self.task_history.append({
            "task": task,
            "response": response,
            "status": "completed"
        })
        return {"result": response, "status": "success"}

    async def get_task_history(self) -> List[Dict[str, Any]]:
        """Retrieve the history of executed tasks."""
        return this.task_history 