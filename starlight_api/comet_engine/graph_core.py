from typing import Any, Dict

from starlight_api.comet_engine.state_kernel import nebula_runtime, OrbitRun
from starlight_api.comet_engine.tool_registry import nebula_tools
from starlight_api.data_models.nebula_schemas import ExecutionLogEntry


def execute_run_to_completion(run_id: str) -> OrbitRun:
    """
    Execute a workflow run until it finishes.
    - Follows the edges defined in the FlowMap.
    - At each node, calls the corresponding tool from the registry.
    - Stops when:
        * there is no next node, OR
        * the state contains stop=True (simple branching/stop condition).
    """
    orbit = nebula_runtime.get_run(run_id)
    graph = nebula_runtime.get_graph(orbit.graph_id)

    step_counter = len(orbit.log)

    while not orbit.finished and orbit.current_node is not None:
        node_key = orbit.current_node

        # resolve which tool to call for this node
        if node_key not in graph.nodes:
            # If node not found in mapping, stop gracefully
            orbit.finished = True
            orbit.current_node = None
            break

        tool_name = graph.nodes[node_key]
        tool_func = nebula_tools.get(tool_name)

        # Execute the tool with the current state
        new_state: Dict[str, Any] = tool_func(dict(orbit.state))
        orbit.state = new_state

        # Log this step
        orbit.log.append(
            ExecutionLogEntry(
                step=step_counter,
                node=node_key,
                tool=tool_name,
                state_snapshot=dict(orbit.state),
            )
        )
        step_counter += 1

        # Branching/stop condition: if a tool sets stop=True in state, we exit
        if orbit.state.get("stop", False):
            orbit.finished = True
            orbit.current_node = None
            break

        # Move to next node using edges mapping
        next_node = graph.edges.get(node_key)
        if next_node is None:
            orbit.finished = True
            orbit.current_node = None
        else:
            orbit.current_node = next_node

    return orbit
