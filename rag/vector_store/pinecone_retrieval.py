import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# -----------------------------
# Config
# -----------------------------
INDEX_NAME = "incident-sense"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.70


def retrieve_from_pinecone(summary: str, description: str):
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY not set")

    # 1️⃣ Connect to Pinecone
    pc = Pinecone(api_key=api_key)
    index = pc.Index(INDEX_NAME)

    # 2️⃣ Embed query (STRICT: only summary + description)
    model = SentenceTransformer(EMBEDDING_MODEL)
    query_text = f"{summary} {description}"

    query_vector = model.encode(query_text).tolist()

    # 3️⃣ Query Pinecone
    result = index.query(
        vector=query_vector,
        top_k=1,
        include_metadata=True
    )

    if not result["matches"]:
        return {
            "match_found": False,
            "confidence": 0.0,
            "root_cause": "No history found. Please proceed with manual analysis.",
            "resolution": "No history found. Please proceed with manual analysis."
        }

    match = result["matches"][0]
    score = match["score"]

    # 4️⃣ Threshold decision
    if score >= SIMILARITY_THRESHOLD:
        metadata = match["metadata"]

        return {
            "match_found": True,
            "confidence": round(score, 2),
            "incident_id": metadata.get("incident_id"),
            "root_cause": metadata.get("root_cause"),
            "resolution": metadata.get("resolution")
        }

    else:
        return {
            "match_found": False,
            "confidence": round(score, 2),
            "root_cause": "No history found. Please proceed with manual analysis.",
            "resolution": "No history found. Please proceed with manual analysis."
        }


# -----------------------------
# Local Test
# -----------------------------
if __name__ == "__main__":
    test_summary = "Email service issue"
    test_description = "Users reported issues related to email service affecting normal operations"

    response = retrieve_from_pinecone(
        summary=test_summary,
        description=test_description
    )

    print("\n🔍 Pinecone Retrieval Result:\n")
    print(response)
