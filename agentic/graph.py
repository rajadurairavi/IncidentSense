from langgraph.graph import StateGraph, END
from agentic.state import GraphState
from agentic.nodes.summary_node import summary_node
from agentic.nodes.retrieval_node import retrieval_node
from agentic.nodes.decision_node import decision_node
from agentic.nodes.response_known_node import response_known_node
from agentic.nodes.response_manual_node import response_manual_node

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("summary", summary_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("known_response", response_known_node)
    graph.add_node("manual_response", response_manual_node)

    graph.set_entry_point("summary")
    graph.add_edge("summary", "retrieval")

    graph.add_conditional_edges(
        "retrieval",
        decision_node,
        {
            "known": "known_response",
            "manual": "manual_response"
        }
    )

    graph.add_edge("known_response", END)
    graph.add_edge("manual_response", END)

    return graph.compile()
