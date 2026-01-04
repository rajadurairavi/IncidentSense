import os
from agentic.state import GraphState
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

SYSTEM_PROMPT = """
You are an ITSM incident response assistant.

You are given FACTS retrieved from historical incidents.
These facts are authoritative.

STRICT RULES:
- Use ONLY the provided facts.
- Do NOT add new root causes.
- Do NOT add new resolution steps.
- Do NOT generalize or guess.
- Do NOT use external knowledge.
- If something is not present in the facts, do NOT mention it.

If the facts are insufficient, respond exactly with:
"Insufficient historical data to provide a definitive root cause or resolution."

Format the response EXACTLY as below:

Incident Summary:
<one concise sentence>

Root Cause:
<root cause exactly as provided>

Resolution Steps:
<numbered steps based ONLY on provided resolution>

FACTS:
{facts}
"""

def response_known_node(state: GraphState) -> GraphState:
    facts = f"""
FACTS:
Root Cause:
{state['root_cause']}

Resolution:
{state['resolution']}
"""

    question = f"""
Incident:
Summary: {state['user_summary']}
Description: {state['user_description']}
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"{question}\n\n{facts}")
    ]

    response = llm.invoke(messages)

    state["final_response"] = {
        "incident": {
            "summary": state["user_summary"],
            "description": state["user_description"]
        },
        "based_on_history": True,
        "confidence": state["confidence"],
        "answer": response.content
    }

    return state
