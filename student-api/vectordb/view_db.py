# view_vector_db.py
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="students")

# Get everything stored (ids, metadata, embeddings)
data = collection.get(include=["embeddings", "metadatas", "documents"])

print(f"Total vectors stored: {len(data['ids'])}\n")

for i in range(len(data["ids"])):
    print(f"ID: {data['ids'][i]}")
    print(f"Metadata: {data['metadatas'][i]}")
    print(f"Embedding (first 5 values): {data['embeddings'][i][:5]}...")
    print(f"Embedding length: {len(data['embeddings'][i])}")
    print("-" * 50)