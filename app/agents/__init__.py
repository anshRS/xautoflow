from app.agents.planner_agent import PlannerAgent
from app.agents.research_agent import ResearchAgent
from app.agents.strategy_agent import StrategyAgent
from app.agents.backtest_agent import BacktestAgent
from app.agents.coordinator_agent import CoordinatorAgent

def create_planner_agent():
    """Create a planner agent for generating workflow plans."""
    return PlannerAgent()

def create_research_agent():
    """Create a research agent for financial research tasks."""
    return ResearchAgent()

def create_strategy_agent():
    """Create a strategy agent for developing trading strategies."""
    return StrategyAgent()

def create_backtest_agent():
    """Create a backtest agent for testing trading strategies."""
    return BacktestAgent()

def create_coordinator_agent():
    """Create a coordinator agent for managing agent interactions."""
    return CoordinatorAgent() 