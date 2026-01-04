from pinecone import Pinecone
import os

INDEX_NAME = "incident-sense"

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

if INDEX_NAME in [i.name for i in pc.list_indexes()]:
    pc.delete_index(INDEX_NAME)
    print("✅ Pinecone index deleted:", INDEX_NAME)
else:
    print("ℹ️ Index not found, nothing to delete")
