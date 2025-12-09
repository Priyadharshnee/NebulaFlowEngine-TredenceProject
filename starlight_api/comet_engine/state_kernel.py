from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from starlight_api.data_models.nebula_schemas import (
    ExecutionLogEntry,
    generate_id,
)


@dataclass
class FlowMap:
    graph_id: str
    name: str
    nodes: Dict[str, str]          # node_key -> tool_name
    edges: Dict[str, str]          # node_key -> next_node_key
    start_node: str


@dataclass
class OrbitRun:
    run_id: str
    graph_id: str
    current_node: Optional[str]
    finished: bool = False
    state: Dict[str, Any] = field(default_factory=dict)
    log: List[ExecutionLogEntry] = field(default_factory=list)


class NebulaRuntime:
    """
    Simple in-memory runtime to store graphs (FlowMaps) and runs (OrbitRuns).
    """

    def __init__(self) -> None:
        self._graphs: Dict[str, FlowMap] = {}
        self._runs: Dict[str, OrbitRun] = {}

    # ---- Graph management ----
    def create_graph(self, name: str, nodes: Dict[str, str], edges: Dict[str, str], start_node: str) -> str:
        graph_id = generate_id()
        flow_map = FlowMap(
            graph_id=graph_id,
            name=name,
            nodes=nodes,
            edges=edges,
            start_node=start_node,
        )
        self._graphs[graph_id] = flow_map
        return graph_id

    def get_graph(self, graph_id: str) -> FlowMap:
        if graph_id not in self._graphs:
            raise KeyError(f"Graph '{graph_id}' not found.")
        return self._graphs[graph_id]

    # ---- Run management ----
    def create_run(self, graph_id: str, initial_state: Dict[str, Any]) -> str:
        if graph_id not in self._graphs:
            raise KeyError(f"Graph '{graph_id}' not found.")

        run_id = generate_id()
        graph = self._graphs[graph_id]

        orbit = OrbitRun(
            run_id=run_id,
            graph_id=graph_id,
            current_node=graph.start_node,
            finished=False,
            state=dict(initial_state),
            log=[],
        )
        self._runs[run_id] = orbit
        return run_id

    def get_run(self, run_id: str) -> OrbitRun:
        if run_id not in self._runs:
            raise KeyError(f"Run '{run_id}' not found.")
        return self._runs[run_id]


# Global runtime instance
nebula_runtime = NebulaRuntime()
