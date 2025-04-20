from autogen import UserProxyAgent
from .base_agent import get_base_llm_config

COORDINATOR_PROMPT = """You are a workflow coordinator responsible for:
1. Initiating and managing conversations between agents
2. Ensuring each step in the approved plan is executed
3. Collecting and structuring results
4. Handling errors and reporting status
Always maintain the workflow state and ensure proper data flow between steps."""

def create_coordinator_agent() -> UserProxyAgent:
    return UserProxyAgent(
        name="CoordinatorAgent",
        description=COORDINATOR_PROMPT,
        human_input_mode="NEVER",
        llm_config=get_base_llm_config(),
        code_execution_config={"work_dir": "workspace"}
    )