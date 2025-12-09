from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from starlight_api.data_models.nebula_schemas import (
    GraphCreateRequest,
    GraphCreateResponse,
    GraphRunRequest,
    GraphRunResponse,
    GraphRunStateResponse,
)
from starlight_api.comet_engine.state_kernel import nebula_runtime
from starlight_api.comet_engine.graph_core import execute_run_to_completion
from starlight_api.orbits.summary_orbit import (
    register_aurora_text_tools,
    create_aurora_text_graph,
)

app = FastAPI(
    title="NebulaFlowEngine",
    version="1.0.0",
    docs_url="/docs",   # Swagger UI
    redoc_url="/redoc", # Optional ReDoc UI
)

AURORA_GRAPH_ID: str | None = None


@app.on_event("startup")
def startup_event() -> None:
    """
    On app startup:
    - register all tools
    - create the default Option B summarization graph
    """
    global AURORA_GRAPH_ID

    register_aurora_text_tools()
    AURORA_GRAPH_ID = create_aurora_text_graph()
    print(f"[NebulaFlow] AuroraText graph ready with id: {AURORA_GRAPH_ID}")


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "NebulaFlow is online"}


@app.post("/graph/create", response_model=GraphCreateResponse)
def create_graph(payload: GraphCreateRequest) -> GraphCreateResponse:
    graph_id = nebula_runtime.create_graph(
        name=payload.name,
        nodes=payload.nodes,
        edges=payload.edges,
        start_node=payload.start_node,
    )
    return GraphCreateResponse(graph_id=graph_id)


@app.post("/graph/run", response_model=GraphRunResponse)
def run_graph(payload: GraphRunRequest) -> GraphRunResponse:
    try:
        run_id = nebula_runtime.create_run(
            graph_id=payload.graph_id,
            initial_state=payload.initial_state,
        )
        orbit = execute_run_to_completion(run_id)
        return GraphRunResponse(
            run_id=run_id,
            final_state=orbit.state,
            log=orbit.log,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/graph/state/{run_id}", response_model=GraphRunStateResponse)
def get_graph_state(run_id: str) -> GraphRunStateResponse:
    try:
        orbit = nebula_runtime.get_run(run_id)
        return GraphRunStateResponse(
            run_id=orbit.run_id,
            graph_id=orbit.graph_id,
            current_node=orbit.current_node,
            finished=orbit.finished,
            state=orbit.state,
            log=orbit.log,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.post("/aurora/run", response_model=GraphRunResponse)
def run_aurora_text(initial_state: Dict[str, Any]) -> GraphRunResponse:
    """
    Convenience endpoint to run the default AuroraText Condenser workflow.
    """
    if AURORA_GRAPH_ID is None:
        raise HTTPException(status_code=500, detail="AuroraText graph not initialized.")

    state: Dict[str, Any] = dict(initial_state)
    state.setdefault("chunk_size", 80)
    state.setdefault("per_chunk_words", 25)
    state.setdefault("soft_max_length", 600)
    state.setdefault("summary_limit", 300)

    run_id = nebula_runtime.create_run(AURORA_GRAPH_ID, state)
    orbit = execute_run_to_completion(run_id)

    return GraphRunResponse(
        run_id=run_id,
        final_state=orbit.state,
        log=orbit.log,
    )
