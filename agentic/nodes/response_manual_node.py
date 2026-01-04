from agentic.state import GraphState

def response_manual_node(state: GraphState) -> GraphState:
    state["final_response"] = {
        "incident": {
            "summary": state["user_summary"],
            "description": state["user_description"]
        },
        "based_on_history": False,
        "message": "No historical match found — please analyze manually."
    }
    return state
