from app.agents.planner_agent import create_planner_agent as _create_planner_agent
from app.agents.research_agent import create_research_agent as _create_research_agent
from app.agents.strategy_agent import create_strategy_agent as _create_strategy_agent
from app.agents.backtest_agent import create_backtest_agent as _create_backtest_agent
from app.agents.coordinator_agent import create_coordinator_agent as _create_coordinator_agent

def create_planner_agent():
    """Create a planner agent for generating workflow plans."""
    return _create_planner_agent()

def create_research_agent():
    """Create a research agent for financial research tasks."""
    return _create_research_agent()

def create_strategy_agent():
    """Create a strategy agent for developing trading strategies."""
    return _create_strategy_agent()

def create_backtest_agent():
    """Create a backtest agent for testing trading strategies."""
    return _create_backtest_agent()

def create_coordinator_agent():
    """Create a coordinator agent for managing agent interactions."""
    return _create_coordinator_agent() 