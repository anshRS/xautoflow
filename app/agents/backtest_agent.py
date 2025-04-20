from autogen import AssistantAgent
from .base_agent import get_base_llm_config

BACKTEST_PROMPT = """You are a backtesting specialist. Execute and analyze trading strategy backtests using:
1. Historical market data
2. Strategy parameters and rules
3. VectorBT backtesting engine
Provide detailed analysis of backtest results and performance metrics."""

def create_backtest_agent() -> AssistantAgent:
    return AssistantAgent(
        name="BacktestAgent",
        description=BACKTEST_PROMPT,
        llm_config={
            **get_base_llm_config(),
            "functions": [
                {
                    "name": "run_vectorbt_backtest",
                    "description": "Run a backtest using VectorBT",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data_dict": {
                                "type": "object"
                            },
                            "strategy_params": {
                                "type": "object"
                            },
                            "logic_identifier": {
                                "type": "string"
                            }
                        },
                        "required": ["data_dict", "strategy_params", "logic_identifier"]
                    }
                }
            ]
        }
    )