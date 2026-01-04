from agentic.state import GraphState

def summary_node(state: GraphState) -> GraphState:
    # For now: no LLM, no token usage
    combined = f"{state['user_summary']} {state['user_description']}".strip()
    state["enhanced_summary"] = combined
    return state
