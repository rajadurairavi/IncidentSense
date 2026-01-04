from agentic.graph import build_graph

app = build_graph()

result = app.invoke({
    "user_summary": "Email Service issue",
    "user_description": "Multiple users reported email sending failure"
})

print(result["final_response"])
