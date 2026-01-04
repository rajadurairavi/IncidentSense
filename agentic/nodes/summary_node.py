from agentic.state import IncidentState


def summary_node(state: IncidentState) -> IncidentState:
    """
    Pass-through node.
    Reserved for future normalization or enrichment.
    """
    return state
