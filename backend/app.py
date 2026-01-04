from fastapi import FastAPI
from pydantic import BaseModel

from agentic.graph import build_graph

# Initialize app
app = FastAPI(title="IncidentSense API")

# Build LangGraph once (important)
graph = build_graph()

# Request model
class IncidentRequest(BaseModel):
    summary: str
    description: str

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Main analyze endpoint
@app.post("/analyze")
def analyze_incident(request: IncidentRequest):
    result = graph.invoke({
        "user_summary": request.summary,
        "user_description": request.description
    })

    return result["final_response"]
