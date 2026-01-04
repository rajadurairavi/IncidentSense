import os
from pinecone import Pinecone, ServerlessSpec

# -----------------------------
# Config
# -----------------------------
INDEX_NAME = "incident-sense"
DIMENSION = 384
METRIC = "cosine"


def create_index():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY not set in environment")

    pc = Pinecone(api_key=api_key)

    existing_indexes = [i.name for i in pc.list_indexes()]

    if INDEX_NAME in existing_indexes:
        print(f"✅ Index '{INDEX_NAME}' already exists")
        return

    print(f"🚀 Creating Pinecone index '{INDEX_NAME}'...")

    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    print(f"🎉 Index '{INDEX_NAME}' created successfully!")


if __name__ == "__main__":
    create_index()
