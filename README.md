# **NebulaFlowEngine – Tredence AI Engineering Assignment**

NebulaFlowEngine is a modular and extensible workflow/graph execution engine built using FastAPI and Python.  
It is designed to satisfy the requirements of the Tredence AI Engineering Assignment and demonstrates the following capabilities:

- A minimal workflow execution engine  
- State-driven node transitions  
- Tool/function registry  
- Conditional routing and loop logic  
- Clean REST API interface  
- Complete implementation of **Option B: Summarization + Refinement**  

This backend uses a structured and scalable architecture designed for clarity, modularity, and maintainability.

---

# **Key Features**

## **1. FlowMap Graph Engine**
- Workflows represented as directed graphs  
- Nodes mapped to Python functions (tools)  
- Edges define node-to-node transitions  
- A shared state dictionary flows through all nodes  
- Supports looping and branching using a `stop` flag  

## **2. Tool Registry**
- All node functions are registered globally in `NebulaTools`  
- Tools operate on the same state object  
- Allows flexible extension of new tools without modifying the core engine  

## **3. In-Memory Runtime**
Stores:  
- Graph definitions (`graph_id`)  
- Run details (`run_id`)  
- Current node  
- State snapshots  
- Execution logs  

## **4. FastAPI REST Endpoints**
- `GET /health` – Service health check  
- `POST /graph/create` – Register a workflow graph  
- `POST /graph/run` – Execute a graph until completion  
- `GET /graph/state/{run_id}` – Inspect the current state of a run  
- `POST /aurora/run` – Run the prebuilt Option B workflow  

## **5. Example Workflow – Option B: Summarization + Refinement**
Implements the steps specified in the assignment:

1. Split input text into chunks  
2. Generate concise mini-summaries  
3. Merge mini-summaries  
4. Refine the merged summary  
5. Loop until the summary is under a length threshold  

---

# **Architecture Overview**

```
NebulaFlowEngine/
│
├── starlight_api/
│   ├── main.py                  # FastAPI application and routes
│   │
│   ├── comet_engine/
│   │   ├── graph_core.py        # Core workflow executor
│   │   ├── tool_registry.py     # Tool registry for node functions
│   │   └── state_kernel.py      # In-memory graphs and execution runs
│   │
│   ├── data_models/
│   │   └── nebula_schemas.py    # Pydantic request/response schemas
│   │
│   └── orbits/
│       └── summary_orbit.py     # Option B workflow tools and graph
│
└── README.md
```

---

# **How to Run the Project**

## **1. Install Dependencies**
```bash
pip install fastapi "uvicorn[standard]" pydantic
```

## **2. Start the Server**
```bash
python -m uvicorn starlight_api.main:app --reload
```

## **3. Verify Service Availability**

### Health Check  
```
http://127.0.0.1:8000/health
```

Expected response:
```json
{ "status": "NebulaFlow is online" }
```

### API Documentation (Swagger UI)
```
http://127.0.0.1:8000/docs
```

### ReDoc Documentation  
```
http://127.0.0.1:8000/redoc
```

---

# **Option B Workflow: AuroraText Condenser**

This workflow demonstrates the summarization and refinement process.

### **Nodes and Their Functions**

| Node           | Tool Function     | Purpose                                      |
|----------------|-------------------|----------------------------------------------|
| ShardSplitter  | shard_splitter    | Splits input text into word chunks           |
| EchoSummoner   | echo_summoner     | Produces mini-summaries for each chunk       |
| FusionWeaver   | fusion_weaver     | Combines mini-summaries into one text        |
| ClarityPulse   | clarity_pulse     | Refines and cleans the merged summary        |
| ThresholdGate  | threshold_gate    | Decides whether to stop or continue refining |

### **Looping Logic**
The workflow loops between:

```
ThresholdGate → ClarityPulse → ThresholdGate
```

until this condition becomes true:

```python
state["stop"] = True
```

---

# **Running Option B Workflow**

### Endpoint
```
POST /aurora/run
```

### Example Request
```json
{
  "input_text": "Paste any long article or paragraph here.",
  "summary_limit": 250
}
```

### Response Includes
- `run_id`
- `final_state.final_summary`
- `log` – detailed description of each step executed

---

# **Using the Generic Graph Engine**

## 1. Create a Graph  
```
POST /graph/create
```

Example:
```json
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
```

## 2. Run the Graph  
```
POST /graph/run
```

## 3. Inspect Run State  
```
GET /graph/state/{run_id}
```

---

# **Why This Project Meets the Assignment Requirements**

- Implements a minimal workflow graph engine  
- Uses state as a shared memory across nodes  
- Supports branching and looping  
- Provides all required REST endpoints  
- Includes a complete example workflow (Option B)  
- Implements tool registry and interpreter patterns  
- Built with clear, modular, production-style architecture  

---

# **Potential Future Enhancements**

- Persist graphs and runs in a database  
- Async execution for long-running tools  
- WebSocket-based live execution logs  
- Dynamic conditional branching rules  
- Additional built-in workflows  

---

# **Conclusion**

NebulaFlowEngine is a clean, well-architected backend demonstrating workflow orchestration, state-driven execution, and modular design.  
It fulfills the requirements of the Tredence AI Engineering Assignment while providing room for extensibility and further enhancement.

