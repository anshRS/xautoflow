from typing import Dict, Any
from uuid import UUID
from langgraph.graph import Graph, StateGraph
from app.agents import (
    create_planner_agent,
    create_strategy_agent,
    create_coordinator_agent
)
from app.crud import crud_task
from app.models.task import TaskStatus
from app.workflows.state import WorkflowState

class StrategyWorkflow:
    def __init__(self, task_id: UUID, db_session):
        self.task_id = task_id
        self.db_session = db_session
        self.planner = create_planner_agent()
        self.strategist = create_strategy_agent()
        self.coordinator = create_coordinator_agent()
        self.graph = self._build_graph()

    def _build_graph(self) -> Graph:
        workflow = StateGraph(WorkflowState)

        @workflow.node()
        async def generate_strategy_plan(state: WorkflowState) -> WorkflowState:
            plan_result = await self.planner.generate_plan(
                task_type="STRATEGY_DEV",
                initial_request=state["initial_request"]
            )
            state["current_plan"] = plan_result["plan"]
            
            crud_task.update_task_plan(
                db=self.db_session,
                task_id=self.task_id,
                plan=plan_result["plan"]
            )
            return state

        @workflow.node()
        async def execute_fetch_market_data(state: WorkflowState) -> WorkflowState:
            try:
                result = await self.coordinator.execute_tool(
                    "get_market_data",
                    state["initial_request"]["market_data_params"]
                )
                state["intermediate_results"]["market_data"] = result
            except Exception as e:
                state["error_info"] = {
                    "step": "fetch_market_data",
                    "error": str(e)
                }
            return state

        @workflow.node()
        async def execute_strategy_development(state: WorkflowState) -> WorkflowState:
            try:
                # Calculate indicators
                indicators = await self.coordinator.execute_tool(
                    "calculate_indicators",
                    {
                        "data": state["intermediate_results"]["market_data"],
                        "indicator_config": state["initial_request"]["indicators"]
                    }
                )
                
                # Generate strategy
                strategy = await self.strategist.generate_strategy(
                    market_data=state["intermediate_results"]["market_data"],
                    indicators=indicators,
                    requirements=state["initial_request"]["strategy_requirements"]
                )
                
                # Optimize if requested
                if state["initial_request"].get("optimize_params", False):
                    optimization = await self.coordinator.execute_tool(
                        "optimize_strategy_params",
                        {
                            "strategy_logic_description": strategy["logic"],
                            "data_dict": state["intermediate_results"]["market_data"],
                            "param_space": strategy["param_space"]
                        }
                    )
                    strategy["optimized_params"] = optimization["best_params"]
                
                state["intermediate_results"]["strategy"] = strategy
                
            except Exception as e:
                state["error_info"] = {
                    "step": "strategy_development",
                    "error": str(e)
                }
            return state

        @workflow.node()
        async def finalize_strategy(state: WorkflowState) -> WorkflowState:
            if state.get("error_info"):
                crud_task.update_task_status(
                    db=self.db_session,
                    task_id=self.task_id,
                    status=TaskStatus.FAILED,
                    error_details=state["error_info"]
                )
                return state

            state["final_result"] = {
                "strategy": state["intermediate_results"]["strategy"],
                "market_data_summary": {
                    "period": state["initial_request"]["market_data_params"],
                    "indicators": state["intermediate_results"].get("indicators", {})
                }
            }
            
            crud_task.update_task_status(
                db=self.db_session,
                task_id=self.task_id,
                status=TaskStatus.COMPLETED,
                result=state["final_result"]
            )
            
            return state

        # Edge Conditions
        @workflow.edge()
        def should_continue(state: WorkflowState) -> str:
            if state.get("error_info"):
                return "finalize_strategy"
            
            if not state["plan_approved"]:
                return "wait_for_approval"
            
            if "market_data" not in state["intermediate_results"]:
                return "execute_fetch_market_data"
            
            if "strategy" not in state["intermediate_results"]:
                return "execute_strategy_development"
            
            return "finalize_strategy"

        # Connect nodes
        workflow.add_node("generate_strategy_plan", generate_strategy_plan)
        workflow.add_node("wait_for_approval", lambda x: x)
        workflow.add_node("execute_fetch_market_data", execute_fetch_market_data)
        workflow.add_node("execute_strategy_development", execute_strategy_development)
        workflow.add_node("finalize_strategy", finalize_strategy)

        # Connect edges
        workflow.add_edge("generate_strategy_plan", should_continue)
        workflow.add_edge("wait_for_approval", should_continue)
        workflow.add_edge("execute_fetch_market_data", should_continue)
        workflow.add_edge("execute_strategy_development", should_continue)
        workflow.add_edge("finalize_strategy", lambda _: "end")

        return workflow.compile()

    async def execute(self, initial_state: WorkflowState) -> WorkflowState:
        return await self.graph.ainvoke(initial_state)