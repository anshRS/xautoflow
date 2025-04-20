import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable, Union

import autogen
from autogen import UserProxyAgent, AssistantAgent, Agent, ConversableAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.llm_toolbox import LLMToolkit

from app.core.config import settings, get_llm_config
from app.tools.web_search import web_search
from app.tools.file_tools import read_file, write_file
from app.tools.financial_tools import (
    calculate_technical_indicators, 
    fetch_historical_data,
    optimize_strategy_parameters
)

logger = logging.getLogger(__name__)

# Get LLM configuration
llm_config = get_llm_config()

# Initialize agents container
_agents = {}

def _get_base_llm_config():
    """Create base LLM configuration for agents."""
    config = {
        "config_list": [llm_config],
        "cache_seed": 42,  # For reproducibility and caching
        "temperature": 0.2,  # Lower temperature for more deterministic outputs
    }
    return config

def get_coordinator_agent() -> Agent:
    """Get the coordinator/user proxy agent that interfaces with the API."""
    if "coordinator" not in _agents:
        _agents["coordinator"] = UserProxyAgent(
            name="CoordinatorAgent",
            human_input_mode="NEVER",  # Don't ask for human input in automated workflows
            max_consecutive_auto_reply=10,
            code_execution_config=False,  # Disable code execution for safety
            llm_config=_get_base_llm_config(),
            system_message="""You are the Coordinator Agent that manages user requests and coordinates
            workflows between specialized agents. You interpret user requests, break them down into tasks,
            and manage communication between other agents. You gather results from each agent and
            compile a final response for the user.
            
            Your responsibilities:
            1. Parse user requests and identify required tasks
            2. Coordinate with appropriate specialized agents
            3. Track workflow progress
            4. Compile final results
            5. Maintain a professional, financially-focused tone
            """
        )
    return _agents["coordinator"]

def get_market_research_agent() -> Agent:
    """Get the market research agent."""
    if "market_research" not in _agents:
        # Define common tools for the research agent
        tools = {
            "web_search": web_search,
            "fetch_historical_data": fetch_historical_data
        }
        
        # Create the agent
        _agents["market_research"] = AssistantAgent(
            name="MarketResearchAgent",
            system_message="""You are the Market Research Agent, an expert in analyzing financial markets and gathering
            information about specific stocks and the broader market. You provide comprehensive, factual market
            research by analyzing news, fundamentals, technical data, and market sentiment.
            
            Your capabilities:
            1. Analyzing stock fundamentals (financials, ratios, growth metrics)
            2. Reviewing technical indicators and price trends
            3. Gathering recent news and evaluating market sentiment
            4. Identifying market patterns and potential catalysts
            5. Compiling research findings into a comprehensive analysis
            
            Always provide balanced, objective analysis with supporting evidence. Avoid speculation without
            clear supporting data, and clearly distinguish facts from interpretations.
            """,
            llm_config={
                **_get_base_llm_config(),
                "functions": [
                    {
                        "name": "web_search",
                        "description": "Search the web for information about a stock or market",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "The search query"},
                                "num_results": {"type": "integer", "description": "Number of results to return"}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "fetch_historical_data",
                        "description": "Fetch historical price data for a ticker symbol",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "ticker": {"type": "string", "description": "Ticker symbol"},
                                "period": {"type": "string", "description": "Time period (e.g., '1y', '6mo', '1d')"},
                                "interval": {"type": "string", "description": "Data interval (e.g., '1d', '1h')"}
                            },
                            "required": ["ticker"]
                        }
                    }
                ]
            }
        )
        
        # Register tools with the agent
        for tool_name, tool_func in tools.items():
            _agents["market_research"].register_function(
                function_map={tool_name: tool_func},
                name=tool_name
            )
    
    return _agents["market_research"]

def get_strategy_dev_agent() -> Agent:
    """Get the strategy development agent."""
    if "strategy_dev" not in _agents:
        # Define tools specific to strategy development
        tools = {
            "calculate_technical_indicators": calculate_technical_indicators,
            "optimize_strategy_parameters": optimize_strategy_parameters,
            "write_file": write_file,  # For saving strategy code
            "read_file": read_file,    # For reading templates/examples
        }
        
        # Create the agent
        _agents["strategy_dev"] = AssistantAgent(
            name="StrategyDevAgent",
            system_message="""You are the Strategy Development Agent, an expert in creating and optimizing
            trading strategies based on market research and technical analysis. You design strategies
            tailored to specific market conditions, time horizons, and risk profiles.
            
            Your capabilities:
            1. Designing rules-based trading strategies using technical indicators
            2. Converting market research into actionable trading logic
            3. Generating Python code that implements the strategy
            4. Optimizing strategy parameters
            5. Documenting strategy rationale, rules, and implementation details
            
            You always design strategies that align with the user's specified time horizon, risk profile,
            and constraints. Each strategy should include clear entry/exit rules, risk management guidelines,
            and complete implementation code.
            """,
            llm_config={
                **_get_base_llm_config(),
                "functions": [
                    {
                        "name": "calculate_technical_indicators",
                        "description": "Calculate technical indicators for a price dataset",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "data": {"type": "object", "description": "Price data dictionary or DataFrame as JSON string"},
                                "indicators": {"type": "array", "items": {"type": "string"}, "description": "List of indicators to calculate"}
                            },
                            "required": ["data", "indicators"]
                        }
                    },
                    {
                        "name": "optimize_strategy_parameters",
                        "description": "Find optimal parameters for a trading strategy using historical data",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "strategy_type": {"type": "string", "description": "Type of strategy to optimize"},
                                "parameters_space": {"type": "object", "description": "Dictionary of parameter ranges to search"},
                                "data": {"type": "object", "description": "Historical data for optimization"},
                                "optimization_target": {"type": "string", "description": "Metric to optimize (e.g., 'sharpe_ratio', 'total_return')"}
                            },
                            "required": ["strategy_type", "parameters_space", "data"]
                        }
                    },
                    {
                        "name": "write_file",
                        "description": "Write content to a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filepath": {"type": "string", "description": "Path to write to (must be in allowed directories)"},
                                "content": {"type": "string", "description": "Content to write to the file"}
                            },
                            "required": ["filepath", "content"]
                        }
                    },
                    {
                        "name": "read_file",
                        "description": "Read content from a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filepath": {"type": "string", "description": "Path to read from (must be in allowed directories)"}
                            },
                            "required": ["filepath"]
                        }
                    }
                ]
            }
        )
        
        # Register tools with the agent
        for tool_name, tool_func in tools.items():
            _agents["strategy_dev"].register_function(
                function_map={tool_name: tool_func},
                name=tool_name
            )
    
    return _agents["strategy_dev"]

def get_backtesting_agent() -> Agent:
    """Get the backtesting agent."""
    if "backtesting" not in _agents:
        # Define backtesting-specific tools
        tools = {
            "fetch_historical_data": fetch_historical_data,
            "read_file": read_file,
            "write_file": write_file,  # For saving backtest results
        }
        
        # Create the agent
        _agents["backtesting"] = AssistantAgent(
            name="BacktestingAgent",
            system_message="""You are the Backtesting Agent, an expert in testing trading strategies on
            historical market data to evaluate their performance. You analyze how strategies would have performed
            in past market conditions and provide objective performance metrics.
            
            Your capabilities:
            1. Running backtests on trading strategies using historical data
            2. Calculating key performance metrics (returns, Sharpe ratio, drawdown, etc.)
            3. Analyzing trade logs and identifying patterns in winning/losing trades
            4. Generating performance visualizations
            5. Providing objective analysis of backtest results
            
            Always present backtest results with appropriate context and disclaimers about past performance not
            guaranteeing future results. Identify both strengths and weaknesses in the strategy's performance.
            """,
            llm_config={
                **_get_base_llm_config(),
                # Add function descriptions for backtesting-specific tools
            }
        )
        
        # Register tools with the agent
        for tool_name, tool_func in tools.items():
            _agents["backtesting"].register_function(
                function_map={tool_name: tool_func},
                name=tool_name
            )
    
    return _agents["backtesting"]

def get_rag_enabled_agent() -> Agent:
    """Get an agent with RAG capabilities for querying the knowledge base."""
    if "rag_agent" not in _agents:
        try:
            from app.tools.rag_tools import query_knowledge_base
            
            # Create retrieve user proxy agent with RAG capabilities
            _agents["rag_agent"] = RetrieveUserProxyAgent(
                name="KnowledgeAgent",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=10,
                retrieve_config={
                    "task": "qa",
                    "docs_path": settings.DOCUMENTS_DIR,
                    "custom_query_engine_fn": query_knowledge_base,  # Custom function to query LlamaIndex
                },
                code_execution_config=False,  # Disable code execution
                llm_config=_get_base_llm_config(),
                system_message="""You are the Knowledge Agent with access to a comprehensive financial knowledge base.
                You can retrieve relevant information from the knowledge base to answer questions about financial
                concepts, market data, specific companies, and trading strategies.
                
                When using the knowledge base:
                1. Clearly cite the source of information
                2. Maintain the factual accuracy of the retrieved information
                3. Synthesize information from multiple sources when appropriate
                4. Indicate when information might be outdated or uncertain
                """
            )
        except Exception as e:
            logger.error(f"Failed to initialize RAG agent: {e}")
            # Fallback to regular assistant agent if RAG initialization fails
            _agents["rag_agent"] = AssistantAgent(
                name="KnowledgeAgent",
                system_message="I am a knowledge agent but my RAG capabilities are currently unavailable.",
                llm_config=_get_base_llm_config()
            )
    
    return _agents["rag_agent"]

def create_autogen_group_chat() -> autogen.GroupChat:
    """Create an Autogen GroupChat with all the specialized agents."""
    agents = [
        get_coordinator_agent(),
        get_market_research_agent(),
        get_strategy_dev_agent(),
        get_backtesting_agent(),
        get_rag_enabled_agent()
    ]
    
    group_chat = autogen.GroupChat(
        agents=agents,
        messages=[],
        max_round=15,  # Limit conversation rounds to prevent excessive iterations
        speaker_selection_method="round_robin",  # Or "auto" for dynamic speaker selection
        allow_repeat_speaker=False,  # Discourage the same agent speaking in back-to-back messages
    )
    
    return group_chat

async def run_agent_chat(task_request: Dict[str, Any]) -> Dict[str, Any]:
    """Run a chat between agents to complete a task.
    
    Args:
        task_request: Dictionary containing the task parameters
        
    Returns:
        Dictionary with the results of the agent interaction
    """
    # Format the task as a user request
    task_type = task_request.get("task_type", "")
    request_data = task_request.get("request_data", {})
    
    # Create a properly formatted request message
    if task_type == "research":
        user_request = f"""
        Please conduct market research on {request_data.get('ticker_symbol')} with a {request_data.get('time_horizon')} time horizon.
        Research depth: {request_data.get('research_depth')}
        Focus areas: {', '.join(request_data.get('focus_areas', []))}
        Additional context: {request_data.get('additional_context', 'None')}
        """
    elif task_type == "strategy":
        user_request = f"""
        Please develop a {request_data.get('strategy_type')} trading strategy for {request_data.get('ticker_symbol')} with a {request_data.get('time_horizon')} time horizon.
        Risk profile: {request_data.get('risk_profile')}
        Indicators to include: {', '.join(request_data.get('include_indicators', []))}
        Custom requirements: {request_data.get('custom_requirements', 'None')}
        """
    elif task_type == "backtest":
        user_request = f"""
        Please conduct a backtest for the strategy with ID {request_data.get('strategy_id')} on {request_data.get('ticker_symbol')}.
        Time period: from {request_data.get('start_date')} to {request_data.get('end_date')}
        Initial capital: ${request_data.get('initial_capital', 10000)}
        """
    elif task_type == "end_to_end":
        user_request = f"""
        Please conduct a complete analysis for {request_data.get('ticker_symbol')} with a {request_data.get('time_horizon')} time horizon:
        1. First, conduct market research on the ticker
        2. Then, develop a suitable {request_data.get('strategy_type', 'optimal')} trading strategy 
        3. Finally, backtest the strategy
        
        Risk profile: {request_data.get('risk_profile')}
        Additional requirements: {request_data.get('custom_requirements', 'None')}
        """
    else:
        return {"error": "Unsupported task type"}
    
    try:
        # Create a group chat with all agents
        group_chat = create_autogen_group_chat()
        
        # Get the coordinator to initiate the chat
        coordinator = get_coordinator_agent()
        
        # Create a manager to run the chat
        manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=_get_base_llm_config())
        
        # Run the chat asynchronously using asyncio.to_thread to not block
        # Note: Autogen might not be fully async-compatible, so we use a thread
        result = await asyncio.to_thread(
            coordinator.initiate_chat, 
            manager,
            message=user_request,
            clear_history=True
        )
        
        # Extract results from the chat
        chat_history = group_chat.messages
        final_answer = chat_history[-1]["content"] if chat_history else "No results generated"
        
        return {
            "success": True,
            "result": final_answer,
            "chat_history": chat_history,
            "origin_task": task_request
        }
    
    except Exception as e:
        logger.error(f"Error running agent chat: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "origin_task": task_request
        } 