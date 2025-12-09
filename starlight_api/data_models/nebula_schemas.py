from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class GraphCreateRequest(BaseModel):
    name: str = Field(..., description="Human readable name of the graph")
    nodes: Dict[str, str] = Field(
        ..., description="Mapping from node key to tool name (function id)"
    )
    edges: Dict[str, str] = Field(
        ..., description="Mapping from node key to next node key"
    )
    start_node: str = Field(..., description="Name of the starting node")


class GraphCreateResponse(BaseModel):
    graph_id: str


class ExecutionLogEntry(BaseModel):
    step: int
    node: str
    tool: str
    state_snapshot: Dict[str, Any]


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="Initial shared state for the workflow run",
    )


class GraphRunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    log: List[ExecutionLogEntry]


class GraphRunStateResponse(BaseModel):
    run_id: str
    graph_id: str
    current_node: Optional[str]
    finished: bool
    state: Dict[str, Any]
    log: List[ExecutionLogEntry]


def generate_id() -> str:
    """Generate a simple unique id for graphs and runs."""
    return str(uuid.uuid4())
