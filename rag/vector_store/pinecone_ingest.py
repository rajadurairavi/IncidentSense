import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# -----------------------------
# Config
# -----------------------------
INDEX_NAME = "incident-sense"
CSV_PATH = "data/helix_incidents_1000.csv"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def ingest_csv_to_pinecone():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY not set in environment")

    print("🔌 Connecting to Pinecone...")
    pc = Pinecone(api_key=api_key)
    index = pc.Index(INDEX_NAME)

    print("📥 Loading CSV...")
    df = pd.read_csv(CSV_PATH)
    df = df.fillna("")

    print(f"📊 Total incidents: {len(df)}")

    print("🧠 Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    vectors = []

    for _, row in df.iterrows():
        # STRICT MODE: embed only summary + description
        text_to_embed = f"{row['summary']} {row['description']}"

        embedding = model.encode(text_to_embed).tolist()

        vector = {
            "id": row["incident_id"],
            "values": embedding,
            "metadata": {
                "incident_id": row["incident_id"],
                "root_cause": row["root_cause"],
                "resolution": row["resolution"],
                "category": row.get("category", ""),
                "service": row.get("service", "")
            }
        }

        vectors.append(vector)

    print("⬆️ Uploading vectors to Pinecone...")
    index.upsert(vectors=vectors)

    print("🎉 Ingestion completed successfully!")


if __name__ == "__main__":
    ingest_csv_to_pinecone()
