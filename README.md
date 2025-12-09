#NebulaFlowEngine – Tredence AI Engineering Assignment

NebulaFlowEngine is a modular and extensible workflow/graph execution engine built with FastAPI and Python, created as part of the Tredence AI Engineering assignment.
It demonstrates:

A minimal workflow execution engine

State-driven node transitions

Tool/function registry

Conditional routing and loop logic

Clean REST API interfaces

A complete implementation of Option B: Summarization + Refinement as required in the assignment

This backend uses a structured architecture designed for clarity, modularity, and extensibility.

Key Features
1. FlowMap Graph Engine

Workflows represented as directed graphs

Nodes mapped to Python functions (tools)

Edges define node-to-node transitions

A shared state dictionary flows through all nodes

Looping and branching supported through a stop-flag mechanism

2. Tool Registry

All node functions (tools) are registered globally in NebulaTools

Each tool reads from and writes to the shared state

3. In-Memory Runtime

Stores:

Graph definitions (graph_id)

Workflow runs (run_id)

Current node, workflow state, and execution logs

4. FastAPI Endpoints

POST /graph/create – Create a workflow graph

POST /graph/run – Execute a graph end-to-end

GET /graph/state/{run_id} – Inspect workflow state and logs

GET /health – Basic health check

POST /aurora/run – Run the Option B workflow without manually creating a graph

5. Example Workflow (Option B: Summarization + Refinement)

Implements the required workflow:

Split input text into chunks

Generate mini-summaries

Merge summaries

Refine the merged summary

Loop until the summary is shorter than a given threshold

This demonstrates state evolution, transitions, looping, and conditional routing.

Project Structure
NebulaFlowEngine/
├── starlight_api/
│   ├── main.py                   # FastAPI routes and startup
│   ├── comet_engine/
│   │   ├── graph_core.py         # Workflow executor
│   │   ├── tool_registry.py      # Global tool registry
│   │   └── state_kernel.py       # In-memory runtime & models
│   ├── data_models/
│   │   └── nebula_schemas.py     # Pydantic request/response models
│   └── orbits/
│       └── summary_orbit.py      # Option B tools and graph definition
└── README.md

How to Run Locally
1. Install Dependencies
pip install fastapi "uvicorn[standard]" pydantic

2. Start the Server
python -m uvicorn starlight_api.main:app --reload

3. Verify Server

Health check:
http://127.0.0.1:8000/health

Swagger Documentation (UI):
http://127.0.0.1:8000/docs

ReDoc Documentation:
http://127.0.0.1:8000/redoc

Option B Workflow: AuroraText Condenser

This workflow follows the assignment specification for summarization + refinement.

Workflow Nodes
Node	Tool Name	Purpose
ShardSplitter	shard_splitter	Splits text into word-based chunks
EchoSummoner	echo_summoner	Generates per-chunk mini summaries
FusionWeaver	fusion_weaver	Merges mini summaries into one string
ClarityPulse	clarity_pulse	Cleans and trims the merged summary
ThresholdGate	threshold_gate	Checks length and loops if needed
Loop Logic

If the summary exceeds the configured limit, execution loops:

ThresholdGate → ClarityPulse → ThresholdGate → ...


Loop terminates when:

state["stop"] = True

Running Option B Workflow

Endpoint:
POST /aurora/run

Example request:

{
  "input_text": "Paste any long article or text here.",
  "summary_limit": 250
}


Example response includes:

final_state.final_summary

run_id

Full node-by-node execution log

Using the Generic Graph Engine
1. Create a Graph
POST /graph/create


Example:

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

2. Run the Graph
POST /graph/run

3. Check State
GET /graph/state/{run_id}





