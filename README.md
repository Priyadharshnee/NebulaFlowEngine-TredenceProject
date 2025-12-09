🚀 NebulaFlowEngine – Tredence AI Engineering Assignment

NebulaFlowEngine is a modular and extensible workflow/graph execution engine built with FastAPI and Python, designed as part of the Tredence AI Engineering Assignment.
It demonstrates how to build:

A minimal, reusable workflow engine

State-driven node execution

Conditional routing & looping

Tool registries

Clean API interfaces

A complete example workflow (Option B: Summarization + Refinement) as required in the assignment.

This project uses a unique naming theme (NebulaFlow + Aurora workflow) but follows exactly the functional requirements specified in the assignment.
Key Features
🔹 1. FlowMap Graph Engine

Defines workflows as graphs:

Nodes → specific processing steps

Edges → transitions between steps

Start node → entry point

Simple and powerful design using Python dictionaries.

🔹 2. NebulaTools Registry

All node functions (tools) are registered globally.

Tools operate on and update a shared state dictionary.

🔹 3. State-Based Execution

Every node receives and returns the same state dictionary.

State evolves as the workflow progresses.

Looping/branching handled through state["stop"].

🔹 4. In-Memory Runtime

Stores:

Graphs (graph_id)

Workflow runs (run_id)

Current node, full state, and execution log

🔹 5. FastAPI Endpoints

REST APIs as required:

POST /graph/create – Create a new workflow graph

POST /graph/run – Run a graph end-to-end

GET /graph/state/{run_id} – Inspect current state & logs

GET /health – Simple health check

POST /aurora/run – Run the Option-B summarization workflow

🔹 6. Example Workflow (Option B – Summarization + Refinement)

Implements the exact sequence required in the assignment:

Split text into chunks

Generate chunk summaries

Merge summaries
Architecture OverviewNebulaFlowEngine/
│
├── starlight_api/
│   ├── main.py                   # FastAPI app & endpoints
│   │
│   ├── comet_engine/
│   │   ├── graph_core.py         # Engine executor
│   │   ├── tool_registry.py      # Global registry for tools
│   │   └── state_kernel.py       # In-memory graphs & runs
│   │
│   ├── data_models/
│   │   └── nebula_schemas.py     # Pydantic models
│   │
│   └── orbits/
│       └── summary_orbit.py      # Option-B workflow tools + graph
│
└── README.md
How to Run the Project Locally
1️⃣ Install Dependencies
pip install fastapi "uvicorn[standard]" pydantic

2️⃣ Run the API Server
python -m uvicorn starlight_api.main:app --reload

3️⃣ Verify the Server

Health Check
👉 http://127.0.0.1:8000/health

Response:

{ "status": "NebulaFlow is online" }


Full API Documentation (Swagger UI)
👉 http://127.0.0.1:8000/docs

Alternative Documentation (ReDoc)
👉 http://127.0.0.1:8000/redoc

🌟 Option B Workflow (AuroraText Condenser)

This is the required sample workflow from the assignment.

Workflow Nodes
Node	Tool Name	Purpose
ShardSplitter	shard_splitter	Splits input text into chunks
EchoSummoner	echo_summoner	Creates mini-summaries
FusionWeaver	fusion_weaver	Merges mini-summaries
ClarityPulse	clarity_pulse	Cleans/refines summary
ThresholdGate	threshold_gate	Loop decision (stop or refine)
Loop Logic

If len(final_summary) > summary_limit, engine loops:

ThresholdGate → ClarityPulse → ThresholdGate → ...


Loop ends when:

state["stop"] = True

 How to Run Option B Workflow

Use Swagger UI /docs or send a POST request to:

POST /aurora/run
Example Body:
{
  "input_text": "Paste any long article or paragraph here...",
  "summary_limit": 250
}

Example Output:

final_state.final_summary – refined summary

run_id – execution ID

log – detailed node-by-node trace

Generic Graph Engine Usage
Create a Graph Manually

POST /graph/create

{
  "name": "MyFlow",
  "nodes": {
    "Start": "shard_splitter",
    "Next": "echo_summoner"
  },
  "edges": {
    "Start": "Next"
  },
  "start_node": "Start"
}

Run That Graph

POST /graph/run

{
  "graph_id": "returned_graph_id_here",
  "initial_state": {
    "input_text": "Hello world!"
  }
}

Check Run State

GET /graph/state/{run_id}

Why This Project Meets the Assignment Requirements

This backend satisfies all core requirements in the assignment summary:

Minimal workflow / graph engine ✔

Nodes with shared state ✔

Edges defining transitions ✔

Branching & looping ✔

Tool registry ✔

FastAPI endpoints ✔

Complete example workflow (Option B) ✔

Clean, modular folder structure ✔

What Can Be Improved With More Time

Add database persistence instead of in-memory runtime

Add async support for long-running tools

Add WebSocket live log streaming

Add dynamic branching rules in JSON format

Add more sample workflows (e.g., code review, anomaly detection)

Conclusion

NebulaFlowEngine showcases a clean and extensible approach to workflow orchestration using Python and FastAPI.
It meets the assignment’s functional requirements while offering a unique naming system and modular architecture ideal for showcasing backend engineering capability.

Refine the summary

Loop until under a length threshold
