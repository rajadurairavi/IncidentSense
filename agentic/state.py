from typing import TypedDict, Optional


class IncidentState(TypedDict, total=False):
    # User input (only description now)
    description: str

    # Retrieval outputs
    match_found: bool
    confidence: float
    root_cause: Optional[str]
    resolution: Optional[str]

    # Final response
    final_response: dict
