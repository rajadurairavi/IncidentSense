from agentic.state import GraphState

def decision_node(state: GraphState) -> str:
    return "known" if state.get("match_found") else "manual"
