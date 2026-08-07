# vector_store.py
import chromadb
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _client.get_or_create_collection(
    name="students",
    metadata={"hnsw:space": "cosine"},
)


def _embed(text: str):
    return _model.encode(text).tolist()


def upsert_student_vector(student_id: int, name: str, email: str):
    text = f"{name} {email}"
    _collection.upsert(
        ids=[str(student_id)],
        embeddings=[_embed(text)],
        metadatas=[{"student_id": student_id, "name": name, "email": email}],
    )


def delete_student_vector(student_id: int):
    _collection.delete(ids=[str(student_id)])


def search_students_vector(query: str, top_k: int = 10, threshold: float = 0.5):
    results = _collection.query(query_embeddings=[_embed(query)], n_results=top_k)
    if not results["ids"][0]:
        return []

    matches = []
    for _id, distance, meta in zip(
        results["ids"][0], results["distances"][0], results["metadatas"][0]
    ):
        similarity = 1 - distance
        if similarity >= threshold:
            matches.append({**meta, "score": round(similarity, 4)})

    return sorted(matches, key=lambda x: -x["score"])