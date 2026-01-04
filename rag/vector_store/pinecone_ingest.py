import os
import pandas as pd
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# -----------------------------
# Config
# -----------------------------
INDEX_NAME = "incident-sense"
CSV_PATH = "data/helix_incidents_1000.csv"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 100

# -----------------------------
# Ingest Function
# -----------------------------
def ingest_csv_to_pinecone():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY not set")

    print("🔌 Connecting to Pinecone...")
    pc = Pinecone(api_key=api_key)
    index = pc.Index(INDEX_NAME)

    print("📄 Loading CSV...")
    df = pd.read_csv(CSV_PATH)
    print(f"📊 Total incidents: {len(df)}")

    print("🧠 Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    vectors = []

    for i, row in tqdm(df.iterrows(), total=len(df)):
        description = str(row["description"])

        embedding = model.encode(description).tolist()

        metadata = {
            "incident_id": row.get("incident_id", f"INC{i}"),
            "root_cause": row.get("root_cause", ""),
            "resolution": row.get("resolution", "")
        }

        vectors.append({
            "id": f"incident-{i}",
            "values": embedding,
            "metadata": metadata
        })

        if len(vectors) >= BATCH_SIZE:
            index.upsert(vectors)
            vectors.clear()

    if vectors:
        index.upsert(vectors)

    print("🎉 Ingestion completed successfully!")


if __name__ == "__main__":
    ingest_csv_to_pinecone()
