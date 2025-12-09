from typing import Any, Dict, List

from starlight_api.comet_engine.tool_registry import nebula_tools
from starlight_api.comet_engine.state_kernel import nebula_runtime


# ========== TOOL IMPLEMENTATIONS ==========

def shard_splitter(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Split input_text into chunks of words.
    Expects in state:
        input_text: str
        chunk_size: int (number of words per chunk, default 80)
    """
    text = state.get("input_text", "")
    if not isinstance(text, str):
        text = str(text)

    chunk_size = int(state.get("chunk_size", 80))

    words = text.split()
    chunks: List[str] = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())

    state["chunks"] = chunks
    return state


def echo_summoner(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a simple summary for each chunk.
    Strategy: take the first N words as a 'mini-summary'.
    Expects:
        chunks: List[str]
        per_chunk_words: int (default 25)
    """
    chunks: List[str] = state.get("chunks", [])
    per_chunk_words = int(state.get("per_chunk_words", 25))

    chunk_summaries: List[str] = []

    for chunk in chunks:
        words = chunk.split()
        shortened = " ".join(words[:per_chunk_words])
        chunk_summaries.append(shortened.strip())

    state["chunk_summaries"] = chunk_summaries
    return state


def fusion_weaver(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge all chunk summaries into a single combined summary.
    """
    summaries: List[str] = state.get("chunk_summaries", [])
    merged = ". ".join(s.strip() for s in summaries if s.strip())
    state["merged_summary"] = merged
    return state


def clarity_pulse(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Refine the merged summary a bit:
    - Normalize spaces
    - Optionally trim to a soft max length
    Expects:
        merged_summary: str
        soft_max_length: int (default 600 characters)
    """
    summary = state.get("merged_summary", "") or ""
    if not isinstance(summary, str):
        summary = str(summary)

    # Basic cleanup
    refined = " ".join(summary.split())

    soft_max_length = int(state.get("soft_max_length", 600))
    if len(refined) > soft_max_length:
        refined = refined[:soft_max_length].rsplit(" ", 1)[0].strip()

    state["final_summary"] = refined
    return state


def threshold_gate(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decide whether to stop or continue refining based on summary length.
    Expects:
        final_summary: str
        summary_limit: int (hard limit, default 300 characters)
    If len(final_summary) <= summary_limit -> stop=True
    Else -> keep going (loop back to ClarityPulse via graph edges)
    """
    summary = state.get("final_summary", "") or ""
    if not isinstance(summary, str):
        summary = str(summary)

    limit = int(state.get("summary_limit", 300))

    if len(summary) <= limit:
        # Signal the engine to stop
        state["stop"] = True
    else:
        # Optionally we can adjust parameters for another pass
        # e.g., tighten soft_max_length a bit each iteration
        current_soft_max = int(state.get("soft_max_length", 600))
        state["soft_max_length"] = max(limit, current_soft_max - 50)

    return state


# ========== REGISTRATION & GRAPH CREATION ==========

def register_aurora_text_tools() -> None:
    """
    Register all AuroraText Condenser tools in the global NebulaTools registry.
    """
    nebula_tools.register("shard_splitter", shard_splitter)
    nebula_tools.register("echo_summoner", echo_summoner)
    nebula_tools.register("fusion_weaver", fusion_weaver)
    nebula_tools.register("clarity_pulse", clarity_pulse)
    nebula_tools.register("threshold_gate", threshold_gate)


def create_aurora_text_graph() -> str:
    """
    Create the Option B (Summarization + Refinement) workflow graph in the runtime.

    Nodes (unique names):
        ShardSplitter  -> shard_splitter
        EchoSummoner   -> echo_summoner
        FusionWeaver   -> fusion_weaver
        ClarityPulse   -> clarity_pulse
        ThresholdGate  -> threshold_gate

    Edges:
        ShardSplitter -> EchoSummoner
        EchoSummoner  -> FusionWeaver
        FusionWeaver  -> ClarityPulse
        ClarityPulse  -> ThresholdGate
        ThresholdGate -> ClarityPulse   (loop until stop=True)
    """
    nodes = {
        "ShardSplitter": "shard_splitter",
        "EchoSummoner": "echo_summoner",
        "FusionWeaver": "fusion_weaver",
        "ClarityPulse": "clarity_pulse",
        "ThresholdGate": "threshold_gate",
    }

    edges = {
        "ShardSplitter": "EchoSummoner",
        "EchoSummoner": "FusionWeaver",
        "FusionWeaver": "ClarityPulse",
        "ClarityPulse": "ThresholdGate",
        # Loop edge: gate sends back to ClarityPulse unless stop=True
        "ThresholdGate": "ClarityPulse",
    }

    graph_id = nebula_runtime.create_graph(
        name="AuroraText Condenser (Option B Summarization)",
        nodes=nodes,
        edges=edges,
        start_node="ShardSplitter",
    )
    return graph_id
