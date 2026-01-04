import os
from agentic.state import IncidentState
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

PROMPT = """
You are an ITSM incident response assistant.

You are given FACTS retrieved from historical incidents.
These facts are authoritative.

STRICT RULES:
- Use ONLY the provided facts.
- Do NOT add new root causes.
- Do NOT add new resolution steps.
- Do NOT assume or generalize.
- Do NOT use external knowledge.

If the facts are insufficient, respond exactly with:
"Insufficient historical data to provide a definitive root cause or resolution."

Format the response EXACTLY as below:

Root Cause:
<root cause exactly as provided>

Resolution Steps:
<numbered steps based ONLY on provided resolution>

"""

def response_known_node(state: IncidentState) -> IncidentState:
    facts = f"""
Root Cause: {state.get('root_cause')}
Resolution: {state.get('resolution')}
"""

    question = f"""
Incident Description:
{state["description"]}
"""

    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(content=question + "\n\n" + facts)
    ]

    response = llm.invoke(messages)

    state["final_response"] = {
        "based_on_history": True,
        "confidence": state["confidence"],
        "answer": response.content
    }

    return state
