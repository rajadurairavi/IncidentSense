from agentic.state import IncidentState


def response_manual_node(state: IncidentState) -> IncidentState:
    state["final_response"] = {
        "based_on_history": False,
        "message": "No historical match found — please analyze manually."
    }
    return state
