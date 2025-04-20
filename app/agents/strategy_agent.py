from autogen import AssistantAgent
from .base_agent import get_base_llm_config
from app.tools.indicator_tools import calculate_indicators

STRATEGY_PROMPT = """You are a quantitative strategist. Design trading strategies based on:
1. Research context and market analysis
2. User requirements (indicators, risk tolerance)
3. Technical analysis using available indicators
Define clear entry/exit rules and prepare parameter spaces for optimization."""

def create_strategy_agent() -> AssistantAgent:
    return AssistantAgent(
        name="StrategyAgent",
        description=STRATEGY_PROMPT,
        llm_config={
            **get_base_llm_config(),
            "functions": [
                {
                    "name": "calculate_indicators",
                    "description": "Calculate technical indicators for market data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {"type": "object"}
                            },
                            "indicator_config": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["data", "indicator_config"]
                    }
                }
            ]
        }
    )