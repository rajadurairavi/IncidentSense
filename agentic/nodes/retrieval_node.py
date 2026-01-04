from agentic.state import GraphState
from rag.vector_store.pinecone_retrieval import retrieve_from_pinecone

def retrieval_node(state: GraphState) -> GraphState:
    result = retrieve_from_pinecone(
        summary=state["user_summary"],
        description=state["user_description"]
    )

    state["match_found"] = result["match_found"]
    state["confidence"] = result["confidence"]
    state["root_cause"] = result.get("root_cause")
    state["resolution"] = result.get("resolution")

    return state
