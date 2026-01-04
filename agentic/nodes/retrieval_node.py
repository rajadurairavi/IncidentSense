from agentic.state import IncidentState
from rag.vector_store.pinecone_retrieval import retrieve_from_pinecone


def retrieval_node(state: IncidentState) -> IncidentState:
    """
    Calls Pinecone retrieval using ONLY incident description.
    """

    result = retrieve_from_pinecone(
        description=state["description"]
    )

    state["match_found"] = result["match_found"]
    state["confidence"] = result["confidence"]
    state["root_cause"] = result.get("root_cause")
    state["resolution"] = result.get("resolution")

    return state
