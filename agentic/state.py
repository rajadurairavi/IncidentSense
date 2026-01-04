from typing import TypedDict, Optional

class GraphState(TypedDict):
    # User input
    user_summary: str
    user_description: str

    # Processed
    enhanced_summary: Optional[str]

    # Retrieval output
    match_found: Optional[bool]
    confidence: Optional[float]
    root_cause: Optional[str]
    resolution: Optional[str]

    # Final response
    final_response: Optional[dict]
