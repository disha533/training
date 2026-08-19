from sentence_transformers import SentenceTransformer

from schemas.schema import SearchDoc
from db.chromadb import collection

# Loaded once per process and reused for every request.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def _embedding_text(name: str, email: str) -> str:
    """The sentence we turn into a vector for search."""
    return f"{name}, {email}"


def _embed_text(text: str) -> list:
    """Turns text into a 384-number vector."""
    return _model.encode(text).tolist()


def add_doc(doc: SearchDoc):
    embedding = _embed_text(_embedding_text(doc.name, doc.email))

    collection.add(
        ids=[str(doc.id)],
        embeddings=[embedding],
        metadatas=[
            {
                "name": doc.name,
                "email": doc.email,
            }
        ],
    )

    return {"message": "Search doc added successfully"}


def search_docs(
    query: str,
    top_k: int = 10,
    threshold: float = 0.5,
):
    embedding = _embed_text(query)

    result = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["metadatas", "distances"],
    )

    results = []

    ids = result["ids"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]

    for i in range(len(ids)):
        distance = distances[i]

        # Chroma is configured with cosine distance.
        score = 1 - distance

        if score >= threshold:
            results.append(
                {
                    "id": int(ids[i]),
                    "name": metadatas[i]["name"],
                    "email": metadatas[i]["email"],
                    "score": round(score, 4),
                }
            )

    return results