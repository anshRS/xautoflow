from typing import TypedDict, Optional, List, Dict, Any
from uuid import UUID

class WorkflowState(TypedDict):
    task_id: UUID
    initial_request: Dict[str, Any]
    task_type: str
    current_plan: Optional[List[Dict[str, Any]]]
    plan_approved: bool
    agent_inputs: Dict[str, Any]
    agent_outputs: Dict[str, Any]
    intermediate_results: Dict[str, Any]
    final_result: Optional[Dict[str, Any]]
    error_info: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]