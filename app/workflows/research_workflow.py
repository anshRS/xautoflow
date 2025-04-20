from typing import Dict, Any, Optional
from uuid import UUID
from langgraph.graph import Graph, StateGraph
from app.agents import (
    create_planner_agent,
    create_research_agent,
    create_coordinator_agent
)
from app.crud import crud_task
from app.models.task import TaskStatus
from app.workflows.state import WorkflowState

class ResearchWorkflow:
    def __init__(self, task_id: UUID, db_session):
        self.task_id = task_id
        self.db_session = db_session
        self.planner = create_planner_agent()
        self.researcher = create_research_agent()
        self.coordinator = create_coordinator_agent()
        self.graph = self._build_graph()

    def _build_graph(self) -> Graph:
        workflow = StateGraph(WorkflowState)

        # Generate Plan Node
        @workflow.node()
        async def generate_plan(state: WorkflowState) -> WorkflowState:
            plan_result = await self.planner.generate_plan(
                task_type=state["task_type"],
                initial_request=state["initial_request"]
            )
            state["current_plan"] = plan_result["plan"]
            
            await crud_task.update_task_plan(
                db=self.db_session,
                task_id=self.task_id,
                plan=plan_result["plan"]
            )
            return state

        # Dynamic Execution Node
        @workflow.node()
        async def execute_step(state: WorkflowState) -> WorkflowState:
            current_step = state["current_plan"][state.get("current_step_index", 0)]
            
            try:
                result = await self.coordinator.initiate_conversation(
                    self.researcher,
                    f"Execute step: {current_step['node_name']}",
                    current_step["inputs"]
                )
                
                state["intermediate_results"][current_step["node_name"]] = result
                state["current_step_index"] = state.get("current_step_index", 0) + 1
                
            except Exception as e:
                state["error_info"] = {
                    "step": current_step["node_name"],
                    "error": str(e)
                }
            
            return state

        # Finalize Research Node
        @workflow.node()
        async def finalize_research(state: WorkflowState) -> WorkflowState:
            if state.get("error_info"):
                await crud_task.update_task_status(
                    db=self.db_session,
                    task_id=self.task_id,
                    status=TaskStatus.FAILED,
                    error_details=state["error_info"]
                )
                return state

            # Consolidate results
            state["final_result"] = {
                "research_summary": await self.researcher.synthesize_findings(
                    state["intermediate_results"]
                ),
                "detailed_results": state["intermediate_results"]
            }
            
            await crud_task.update_task_status(
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
                return "finalize_research"
            
            if not state["plan_approved"]:
                return "wait_for_approval"
            
            current_index = state.get("current_step_index", 0)
            if current_index >= len(state["current_plan"]):
                return "finalize_research"
            
            return "execute_step"

        # Connect nodes
        workflow.add_node("generate_plan", generate_plan)
        workflow.add_node("wait_for_approval", lambda x: x)
        workflow.add_node("execute_step", execute_step)
        workflow.add_node("finalize_research", finalize_research)

        # Connect edges
        workflow.add_edge("generate_plan", should_continue)
        workflow.add_edge("wait_for_approval", should_continue)
        workflow.add_edge("execute_step", should_continue)
        workflow.add_edge("finalize_research", lambda _: "end")

        return workflow.compile()

    async def execute(self, initial_state: WorkflowState) -> WorkflowState:
        return await self.graph.ainvoke(initial_state)