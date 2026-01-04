from fastapi import FastAPI
from pydantic import BaseModel

from agentic.graph import build_graph

app = FastAPI(title="IncidentSense API")

graph = build_graph()


class IncidentRequest(BaseModel):
    description: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_incident(request: IncidentRequest):
    result = graph.invoke(
        {
            "description": request.description
        }
    )
    return result["final_response"]
