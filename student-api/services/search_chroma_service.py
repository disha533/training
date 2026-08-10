# services/chroma_search_service.py

from fastapi import HTTPException
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


def _insert_vector(
    doc_id: int,
    name: str,
    email: str,
    embedding: list,
):
    collection.add(
        ids=[str(doc_id)],
        embeddings=[embedding],
        metadatas=[
            {
                "name": name,
                "email": email,
            }
        ],
    )


def _delete_vector(doc_id: int):
    collection.delete(
        ids=[str(doc_id)]
    )


def _fetch_vector_by_id(doc_id: int):

    result = collection.get(
        ids=[str(doc_id)],
        include=["metadatas"],
    )

    if not result["ids"]:
        return None

    metadata = result["metadatas"][0]

    return {
        "id": int(result["ids"][0]),
        "name": metadata["name"],
        "email": metadata["email"],
    }


def add_doc(doc: SearchDoc):

    embedding = _embed_text(
        _embedding_text(doc.name, doc.email)
    )

    _insert_vector(
        doc.id,
        doc.name,
        doc.email,
        embedding,
    )

    return {
        "message": "Search doc added successfully"
    }


def get_all_docs():

    result = collection.get(
        include=["metadatas"]
    )

    docs = []

    for i, doc_id in enumerate(result["ids"]):

        metadata = result["metadatas"][i]

        docs.append(
            {
                "id": int(doc_id),
                "name": metadata["name"],
                "email": metadata["email"],
            }
        )

    return docs


def get_doc_by_id(doc_id: int):

    doc = _fetch_vector_by_id(doc_id)

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Search doc not found",
        )

    return doc


def delete_doc(doc_id: int):

    existing = _fetch_vector_by_id(doc_id)

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Search doc not found",
        )

    _delete_vector(doc_id)

    return {
        "message": "Search doc deleted successfully"
    }


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