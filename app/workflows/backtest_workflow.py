from typing import Dict, Any
from uuid import UUID
from langgraph.graph import Graph, StateGraph
from app.agents import (
    create_planner_agent,
    create_backtest_agent,
    create_coordinator_agent
)
from app.crud import crud_task
from app.models.task import TaskStatus
from app.workflows.state import WorkflowState

class BacktestWorkflow:
    def __init__(self, task_id: UUID, db_session):
        self.task_id = task_id
        self.db_session = db_session
        self.planner = create_planner_agent()
        self.backtester = create_backtest_agent()
        self.coordinator = create_coordinator_agent()
        self.graph = self._build_graph()

    def _build_graph(self) -> Graph:
        workflow = StateGraph(WorkflowState)

        @workflow.node()
        async def generate_backtest_plan(state: WorkflowState) -> WorkflowState:
            plan_result = await self.planner.generate_plan(
                task_type="BACKTEST",
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
        async def execute_fetch_backtest_data(state: WorkflowState) -> WorkflowState:
            try:
                result = await self.coordinator.execute_tool(
                    "get_market_data",
                    state["initial_request"]["backtest_data_params"]
                )
                state["intermediate_results"]["market_data"] = result
            except Exception as e:
                state["error_info"] = {
                    "step": "fetch_backtest_data",
                    "error": str(e)
                }
            return state

        @workflow.node()
        async def execute_run_backtest(state: WorkflowState) -> WorkflowState:
            try:
                result = await self.coordinator.execute_tool(
                    "run_vectorbt_backtest",
                    {
                        "data_dict": state["intermediate_results"]["market_data"],
                        "strategy_params": state["initial_request"]["strategy_params"],
                        "logic_identifier": state["initial_request"]["strategy_logic"]
                    }
                )
                state["intermediate_results"]["backtest_results"] = result
            except Exception as e:
                state["error_info"] = {
                    "step": "run_backtest",
                    "error": str(e)
                }
            return state

        @workflow.node()
        async def finalize_backtest(state: WorkflowState) -> WorkflowState:
            if state.get("error_info"):
                crud_task.update_task_status(
                    db=self.db_session,
                    task_id=self.task_id,
                    status=TaskStatus.FAILED,
                    error_details=state["error_info"]
                )
                return state

            state["final_result"] = {
                "backtest_summary": await self.backtester.analyze_results(
                    state["intermediate_results"]["backtest_results"]
                ),
                "detailed_metrics": state["intermediate_results"]["backtest_results"]["metrics"],
                "trades": state["intermediate_results"]["backtest_results"]["trades"]
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
                return "finalize_backtest"
            
            if not state["plan_approved"]:
                return "wait_for_approval"
            
            if "market_data" not in state["intermediate_results"]:
                return "execute_fetch_backtest_data"
            
            if "backtest_results" not in state["intermediate_results"]:
                return "execute_run_backtest"
            
            return "finalize_backtest"

        # Connect nodes
        workflow.add_node("generate_backtest_plan", generate_backtest_plan)
        workflow.add_node("wait_for_approval", lambda x: x)
        workflow.add_node("execute_fetch_backtest_data", execute_fetch_backtest_data)
        workflow.add_node("execute_run_backtest", execute_run_backtest)
        workflow.add_node("finalize_backtest", finalize_backtest)

        # Connect edges
        workflow.add_edge("generate_backtest_plan", should_continue)
        workflow.add_edge("wait_for_approval", should_continue)
        workflow.add_edge("execute_fetch_backtest_data", should_continue)
        workflow.add_edge("execute_run_backtest", should_continue)
        workflow.add_edge("finalize_backtest", lambda _: "end")

        return workflow.compile()

    async def execute(self, initial_state: WorkflowState) -> WorkflowState:
        return await self.graph.ainvoke(initial_state)