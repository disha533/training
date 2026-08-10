
from db.chromadb import collection

result = collection.get(include=["metadatas", "embeddings"])

ids = result["ids"]
metadatas = result["metadatas"]
embeddings = result["embeddings"]

print(f"Total docs stored: {len(ids)}\n")

for doc_id, metadata, embedding in zip(ids, metadatas, embeddings):
    name = metadata["name"]
    email = metadata["email"]
    embedding_length = len(embedding)
    preview = ", ".join(f"{x:.4f}" for x in embedding[:5])

    print(f"ID: {doc_id} | Name: {name} | Email: {email} | Embedding length: {embedding_length}")
    print(f"Embedding preview (first 5 of {embedding_length}): [{preview}, ...]")
    print("-" * 50)