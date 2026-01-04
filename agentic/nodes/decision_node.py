from agentic.state import IncidentState


def decision_node(state: IncidentState) -> str:
    """
    Decides routing based on retrieval result.
    """
    return "known" if state.get("match_found") else "manual"
