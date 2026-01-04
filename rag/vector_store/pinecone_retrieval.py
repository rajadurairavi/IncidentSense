import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# -----------------------------
# Config
# -----------------------------
INDEX_NAME = "incident-sense"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 1
SIMILARITY_THRESHOLD = 0.6

# -----------------------------
# Retrieval Function
# -----------------------------
def retrieve_from_pinecone(description: str):
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY not set")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(INDEX_NAME)

    model = SentenceTransformer(EMBEDDING_MODEL)
    query_embedding = model.encode(description).tolist()

    result = index.query(
        vector=query_embedding,
        top_k=TOP_K,
        include_metadata=True
    )

    if not result["matches"]:
        return {
            "match_found": False,
            "confidence": 0.0,
            "root_cause": None,
            "resolution": None
        }

    match = result["matches"][0]
    score = match["score"]
    print("DEBUG: Pinecone similarity score =", score)


    if score < SIMILARITY_THRESHOLD:
        return {
            "match_found": False,
            "confidence": round(score, 2),
            "root_cause": None,
            "resolution": None
        }

    metadata = match["metadata"]

    return {
        "match_found": True,
        "confidence": round(score, 2),
        "incident_id": metadata.get("incident_id"),
        "root_cause": metadata.get("root_cause"),
        "resolution": metadata.get("resolution")
    }


# -----------------------------
# Local Test
# -----------------------------
if __name__ == "__main__":
    test_description = "Multiple users reported email sending failure"
    response = retrieve_from_pinecone(test_description)
    print(response)
