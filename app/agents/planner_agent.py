from autogen import AssistantAgent
from .base_agent import get_base_llm_config

PLANNER_PROMPT = """You are a meticulous planner for financial analysis tasks. Generate step-by-step plans as JSON lists of dictionaries.
Available node functions: [
    'fetch_market_data',
    'fetch_financial_news',
    'query_knowledge_base',
    'analyze_market_data',
    'synthesize_research',
    'generate_strategy',
    'backtest_strategy'
]
Each node must specify:
- node_name: str
- inputs: Dict[str, str]  # State keys needed
- outputs: Dict[str, str]  # State keys to update
Ensure logical progression towards the goal."""

def create_planner_agent() -> AssistantAgent:
    return AssistantAgent(
        name="PlannerAgent",
        description=PLANNER_PROMPT,  # Using description instead of system_message for Gemini
        llm_config=get_base_llm_config()
    )