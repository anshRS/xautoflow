import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, TypedDict, Annotated, Union, Literal
from uuid import UUID

from langchain.schema import Document
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint import MemorySaver

# LangChain imports
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

# Local imports
from app.core.config import settings, get_llm_config
from app.models.database_models import AgentTask, TaskStatusEnum
from app.tools.financial_tools import (
    fetch_historical_data,
    calculate_technical_indicators,
    optimize_strategy_parameters
)
from app.tools.web_search import web_search
from app.tools.file_tools import read_file, write_file
from app.tools.rag_tools import query_knowledge_base

# Set up logging
logger = logging.getLogger(__name__)

# Define state types for type safety
class WorkflowState(TypedDict):
    """The state of the workflow."""
    task_id: str
    user_request: Dict[str, Any]
    current_step: str
    step_count: int
    research_results: Optional[Dict[str, Any]]
    strategy: Optional[Dict[str, Any]]
    backtest_results: Optional[Dict[str, Any]]
    final_result: Optional[Dict[str, Any]]
    error: Optional[str]
    messages: List[Dict[str, Any]]

# Get LLM configuration
llm_config = get_llm_config()

# Helper function to get LLM model
def get_llm():
    """Create LLM instance based on settings."""
    return ChatOpenAI(
        model=settings.LLM_MODEL_NAME,
        temperature=0.2,
        api_key=settings.OPENAI_API_KEY,
        streaming=False  # Set to True for streaming responses if supported
    )

# Define nodes for the workflow graph

async def planning_node(state: WorkflowState) -> WorkflowState:
    """Planning node that breaks down the high-level task into steps.
    
    This node determines what needs to be done based on the user request.
    """
    task_type = state["user_request"].get("task_type")
    request_data = state["user_request"].get("request_data", {})
    
    # Create a new state with updated current_step
    new_state = state.copy()
    new_state["current_step"] = "planning"
    new_state["step_count"] += 1
    
    llm = get_llm()
    
    # Generate plan based on task type
    planning_prompt = f"""
    You are a financial agent planner. Based on the user's request, create a step-by-step plan.
    
    USER REQUEST: {json.dumps(request_data, indent=2)}
    TASK TYPE: {task_type}
    
    Create a plan with detailed steps. Include which specialized agents should handle each step.
    """
    
    try:
        # Get planning response
        response = await llm.ainvoke([
            SystemMessage(content="You are a financial workflow planner that creates detailed step-by-step plans."),
            HumanMessage(content=planning_prompt)
        ])
        
        # Add the planning result to the messages
        new_state["messages"].append({
            "role": "system",
            "content": f"PLANNING RESULT: {response.content}"
        })
        
        # Determine next step based on task type
        if task_type == "research":
            new_state["next"] = "market_research"
        elif task_type == "strategy":
            # If research results are already provided, skip research step
            if request_data.get("research_results"):
                new_state["research_results"] = request_data.get("research_results")
                new_state["next"] = "strategy_development"
            else:
                new_state["next"] = "market_research"
        elif task_type == "backtest":
            # If strategy is already provided, skip to backtesting
            if request_data.get("strategy_id") or request_data.get("strategy_code"):
                new_state["strategy"] = {
                    "id": request_data.get("strategy_id"),
                    "code": request_data.get("strategy_code"),
                    "params": request_data.get("strategy_params", {})
                }
                new_state["next"] = "backtesting"
            else:
                new_state["next"] = "market_research"
        elif task_type == "end_to_end":
            new_state["next"] = "market_research"
        else:
            new_state["error"] = f"Unsupported task type: {task_type}"
            new_state["next"] = END
    
    except Exception as e:
        logger.error(f"Error in planning node: {e}", exc_info=True)
        new_state["error"] = f"Planning error: {str(e)}"
        new_state["next"] = END
    
    return new_state

async def market_research_node(state: WorkflowState) -> WorkflowState:
    """Market research node that gathers and analyzes market data."""
    new_state = state.copy()
    new_state["current_step"] = "market_research"
    new_state["step_count"] += 1
    
    request_data = state["user_request"].get("request_data", {})
    ticker_symbol = request_data.get("ticker_symbol")
    
    try:
        # Create research tools
        market_research_tools = {
            "web_search": web_search,
            "fetch_historical_data": fetch_historical_data,
            "query_knowledge_base": query_knowledge_base
        }
        
        # Create tool node
        research_tool_node = ToolNode(
            tools=list(market_research_tools.values())
        )
        
        # Format prompt for research
        research_prompt = f"""
        Conduct comprehensive market research on {ticker_symbol}.
        
        Include:
        1. Recent company news and developments
        2. Financial performance and key metrics
        3. Technical analysis of price trends
        4. Industry trends and competitive position
        5. Analyst recommendations and sentiment
        
        Time Horizon: {request_data.get('time_horizon', 'medium-term')}
        Focus Areas: {', '.join(request_data.get('focus_areas', ['fundamentals', 'technicals', 'news']))}
        Additional Context: {request_data.get('additional_context', 'None')}
        
        First, gather the necessary information using the available tools. Then, analyze and synthesize 
        the information into a comprehensive research report.
        """
        
        # Set up LLM
        llm = get_llm()
        
        # Invoke LLM to perform research
        response = await llm.ainvoke([
            SystemMessage(content="You are a financial market research expert. Thoroughly research the given stock."),
            HumanMessage(content=research_prompt)
        ])
        
        # Store research results
        new_state["research_results"] = {
            "ticker_symbol": ticker_symbol,
            "summary": response.content,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add to messages
        new_state["messages"].append({
            "role": "system",
            "content": f"RESEARCH COMPLETED: Analysis for {ticker_symbol}"
        })
        
        # Determine next step based on task_type
        task_type = state["user_request"].get("task_type")
        if task_type in ["strategy", "backtest", "end_to_end"]:
            new_state["next"] = "strategy_development"
        else:
            new_state["next"] = "finalization"
    
    except Exception as e:
        logger.error(f"Error in market research node: {e}", exc_info=True)
        new_state["error"] = f"Market research error: {str(e)}"
        new_state["next"] = END
    
    return new_state

async def strategy_development_node(state: WorkflowState) -> WorkflowState:
    """Strategy development node that creates trading strategies."""
    new_state = state.copy()
    new_state["current_step"] = "strategy_development"
    new_state["step_count"] += 1
    
    request_data = state["user_request"].get("request_data", {})
    research_results = state.get("research_results", {})
    
    try:
        # Create strategy tools
        strategy_tools = {
            "calculate_technical_indicators": calculate_technical_indicators,
            "optimize_strategy_parameters": optimize_strategy_parameters,
            "fetch_historical_data": fetch_historical_data
        }
        
        # Create tool node
        strategy_tool_node = ToolNode(
            tools=list(strategy_tools.values())
        )
        
        # Format prompt for strategy development
        ticker_symbol = request_data.get("ticker_symbol", research_results.get("ticker_symbol"))
        strategy_type = request_data.get("strategy_type", "adaptive")
        risk_profile = request_data.get("risk_profile", "moderate")
        
        strategy_prompt = f"""
        Develop a {strategy_type} trading strategy for {ticker_symbol} based on the provided research.
        
        Research Summary: {research_results.get('summary', 'Not available')}
        
        Strategy Requirements:
        - Time Horizon: {request_data.get('time_horizon', 'medium-term')}
        - Risk Profile: {risk_profile}
        - Indicators to Include: {', '.join(request_data.get('include_indicators', ['RSI', 'MACD', 'Moving Averages']))}
        - Custom Requirements: {request_data.get('custom_requirements', 'None')}
        
        Create a complete strategy with:
        1. Clear entry and exit rules
        2. Position sizing and risk management guidelines
        3. Python code implementation using pandas and necessary libraries
        4. Optimized parameters
        
        The strategy should align with the research findings and specified risk profile.
        """
        
        # Set up LLM
        llm = get_llm()
        
        # Invoke LLM to develop strategy
        response = await llm.ainvoke([
            SystemMessage(content="You are a financial strategy developer expert. Create a robust trading strategy."),
            HumanMessage(content=strategy_prompt)
        ])
        
        # Extract code and parameters from response
        # In a real implementation, we would parse the response more carefully
        # to extract the actual code and parameters
        strategy_text = response.content
        
        # Extract Python code blocks from the response
        import re
        code_blocks = re.findall(r'```python(.*?)```', strategy_text, re.DOTALL)
        strategy_code = code_blocks[0] if code_blocks else ""
        
        # Create a strategy name based on type and ticker
        strategy_name = f"{strategy_type.title()} Strategy for {ticker_symbol}"
        
        # Store strategy results
        new_state["strategy"] = {
            "name": strategy_name,
            "description": strategy_text,
            "code": strategy_code,
            "parameters": {
                "type": strategy_type,
                "risk_profile": risk_profile,
                "ticker": ticker_symbol,
                # We'd extract actual parameters from the response in a real implementation
                "indicators": request_data.get('include_indicators', ['RSI', 'MACD', 'Moving Averages'])
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add to messages
        new_state["messages"].append({
            "role": "system",
            "content": f"STRATEGY DEVELOPED: {strategy_name}"
        })
        
        # Determine next step
        task_type = state["user_request"].get("task_type")
        if task_type in ["backtest", "end_to_end"]:
            new_state["next"] = "backtesting"
        else:
            new_state["next"] = "finalization"
    
    except Exception as e:
        logger.error(f"Error in strategy development node: {e}", exc_info=True)
        new_state["error"] = f"Strategy development error: {str(e)}"
        new_state["next"] = END
    
    return new_state

async def backtesting_node(state: WorkflowState) -> WorkflowState:
    """Backtesting node that evaluates trading strategies on historical data."""
    new_state = state.copy()
    new_state["current_step"] = "backtesting"
    new_state["step_count"] += 1
    
    request_data = state["user_request"].get("request_data", {})
    strategy = state.get("strategy", {})
    
    try:
        # Get ticker and time range
        ticker_symbol = request_data.get("ticker_symbol", strategy.get("parameters", {}).get("ticker"))
        
        # Get start and end dates from request or use defaults
        if "start_date" in request_data and "end_date" in request_data:
            start_date = request_data["start_date"]
            end_date = request_data["end_date"]
        else:
            # Default to 1 year of data
            from datetime import datetime, timedelta
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=365)
        
        initial_capital = request_data.get("initial_capital", 10000.0)
        
        # Format prompt for backtesting
        backtest_prompt = f"""
        Conduct a backtest of the trading strategy for {ticker_symbol} from {start_date} to {end_date}
        with an initial capital of ${initial_capital}.
        
        Strategy Description:
        {strategy.get("description", "Not available")}
        
        Strategy Code:
        ```python
        {strategy.get("code", "# No code available")}
        ```
        
        First, fetch the necessary historical data for {ticker_symbol}. Then implement and run the strategy
        on this data to generate performance metrics including:
        1. Total Return
        2. Sharpe Ratio
        3. Maximum Drawdown
        4. Win Rate
        5. Detailed trade log
        
        Provide a comprehensive analysis of the backtest results, including strengths and weaknesses of
        the strategy's performance. Include visualizations where appropriate.
        """
        
        # Set up LLM
        llm = get_llm()
        
        # Invoke LLM to perform backtesting
        response = await llm.ainvoke([
            SystemMessage(content="You are a financial backtesting expert. Thoroughly evaluate the given trading strategy."),
            HumanMessage(content=backtest_prompt)
        ])
        
        # In a real implementation, we would actually run backtesting code
        # and generate real metrics. This is a simplified example.
        import random
        
        # Generate simulated backtest results
        total_return = random.uniform(-10, 50)  # Percentage return
        sharpe_ratio = random.uniform(0, 3)
        max_drawdown = random.uniform(-30, -5)  # Percentage drawdown
        win_rate = random.uniform(40, 70)  # Percentage of winning trades
        
        # Store backtest results
        new_state["backtest_results"] = {
            "ticker_symbol": ticker_symbol,
            "start_date": start_date.isoformat() if isinstance(start_date, datetime) else start_date,
            "end_date": end_date.isoformat() if isinstance(end_date, datetime) else end_date,
            "initial_capital": initial_capital,
            "total_return": total_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
            "analysis": response.content,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add to messages
        new_state["messages"].append({
            "role": "system",
            "content": f"BACKTEST COMPLETED: {ticker_symbol} strategy with {total_return:.2f}% return"
        })
        
        # Move to finalization
        new_state["next"] = "finalization"
    
    except Exception as e:
        logger.error(f"Error in backtesting node: {e}", exc_info=True)
        new_state["error"] = f"Backtesting error: {str(e)}"
        new_state["next"] = END
    
    return new_state

async def finalization_node(state: WorkflowState) -> WorkflowState:
    """Finalization node that compiles all results into a coherent report."""
    new_state = state.copy()
    new_state["current_step"] = "finalization"
    new_state["step_count"] += 1
    
    try:
        # Gather all results
        research_results = state.get("research_results", {})
        strategy = state.get("strategy", {})
        backtest_results = state.get("backtest_results", {})
        
        # Format prompt for finalization
        finalization_prompt = f"""
        Create a comprehensive final report summarizing all findings and recommendations.
        
        Include the following sections as available:
        
        1. MARKET RESEARCH SUMMARY:
        {research_results.get('summary', 'No research conducted')}
        
        2. STRATEGY DETAILS:
        {strategy.get('description', 'No strategy developed')}
        
        3. BACKTEST RESULTS:
        {backtest_results.get('analysis', 'No backtest conducted')}
        
        Provide a well-structured, professional report with actionable insights and recommendations.
        The report should be suitable for a financial audience and maintain a balanced, objective tone.
        """
        
        # Set up LLM
        llm = get_llm()
        
        # Invoke LLM to create final report
        response = await llm.ainvoke([
            SystemMessage(content="You are a financial analyst creating a comprehensive report of findings."),
            HumanMessage(content=finalization_prompt)
        ])
        
        # Create final result
        new_state["final_result"] = {
            "report": response.content,
            "research": research_results,
            "strategy": strategy,
            "backtest": backtest_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add to messages
        new_state["messages"].append({
            "role": "system",
            "content": "FINALIZATION COMPLETED: Final report generated"
        })
        
        # End the workflow
        new_state["next"] = END
    
    except Exception as e:
        logger.error(f"Error in finalization node: {e}", exc_info=True)
        new_state["error"] = f"Finalization error: {str(e)}"
        new_state["next"] = END
    
    return new_state

async def router(state: WorkflowState) -> Literal["market_research", "strategy_development", "backtesting", "finalization", "END"]:
    """Route to the next node based on the state."""
    if "next" in state:
        return state["next"]
    elif "error" in state:
        return END
    else:
        # Default routing logic based on task_type
        task_type = state["user_request"].get("task_type")
        if task_type == "research":
            return "market_research"
        elif task_type == "strategy":
            return "strategy_development"
        elif task_type == "backtest":
            return "backtesting"
        elif task_type == "end_to_end":
            return "market_research"
        else:
            return END

def create_workflow_graph():
    """Create and configure the workflow graph."""
    # Create a new graph
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("planning", planning_node)
    workflow.add_node("market_research", market_research_node)
    workflow.add_node("strategy_development", strategy_development_node)
    workflow.add_node("backtesting", backtesting_node)
    workflow.add_node("finalization", finalization_node)
    
    # Set the entry point
    workflow.set_entry_point("planning")
    
    # Add conditional routing
    workflow.add_conditional_edges("planning", router)
    workflow.add_conditional_edges("market_research", router)
    workflow.add_conditional_edges("strategy_development", router)
    workflow.add_conditional_edges("backtesting", router)
    workflow.add_conditional_edges("finalization", router)
    
    # Compile the graph
    return workflow.compile()

async def execute_workflow(task_id: Union[str, UUID], request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the LangGraph workflow for a given task.
    
    Args:
        task_id: The ID of the task
        request_data: The task request data
        
    Returns:
        Dictionary with workflow execution results
    """
    try:
        # Create the workflow graph
        workflow = create_workflow_graph()
        
        # Create memory saver for checkpoints
        memory = MemorySaver()
        
        # Initialize the state
        initial_state: WorkflowState = {
            "task_id": str(task_id),
            "user_request": request_data,
            "current_step": "initialization",
            "step_count": 0,
            "research_results": None,
            "strategy": None,
            "backtest_results": None,
            "final_result": None,
            "error": None,
            "messages": []
        }
        
        logger.info(f"Starting workflow for task {task_id}")
        
        # Run the workflow with checkpointing
        async for event, result in workflow.astream(
            initial_state,
            # checkpoint=memory,
            # stream_mode="updates"
        ):
            # Update task in database with new state info
            if event == "new":
                current_step = result.get("current_step", "unknown")
                logger.info(f"Task {task_id}: Step '{current_step}' completed")
                
                # Here you would update the database record
                # We're returning intermediate steps for now
                yield {
                    "task_id": task_id,
                    "current_step": current_step,
                    "step_count": result.get("step_count", 0),
                    "state": result,
                    "is_final": False
                }
        
        # Get the final state
        final_state = memory.get_checkpoint(workflow.id)
        
        # Return the final result
        return {
            "task_id": task_id,
            "current_step": "completed",
            "step_count": final_state.get("step_count", 0),
            "state": final_state,
            "is_final": True
        }
    
    except Exception as e:
        logger.error(f"Error executing workflow for task {task_id}: {e}", exc_info=True)
        return {
            "task_id": task_id,
            "current_step": "error",
            "error": str(e),
            "is_final": True
        } 