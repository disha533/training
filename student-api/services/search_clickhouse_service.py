
#
# Talks directly to ClickHouse. It has no idea Oracle or students exist -
# search docs are their own dataset, created and managed through their
# own endpoints, not derived from student data.
#
#   controller -> service (this file) -> db

from fastapi import HTTPException
from sentence_transformers import SentenceTransformer
from schemas.schema import SearchDoc
from db.clickhouse import client

# Loaded once per process, reused for every request.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def _embedding_text(name: str, email: str) -> str:
    """The sentence we turn into a vector for search."""
    return f"{name}, {email}"


def _embed_text(text: str) -> list:
    """Turns text into a 384-number vector."""
    return _model.encode(text).tolist()


def _insert_vector(doc_id: int, name: str, email: str, embedding: list):
    client.insert(
        "search_docs",
        [[doc_id, name, email, embedding]],
        column_names=["id", "name", "email", "embedding"],
    )


def _delete_vector(doc_id: int):
    client.command(
        "ALTER TABLE search_docs DELETE WHERE id = {id:UInt32}",
        parameters={"id": doc_id},
    )


def _fetch_vector_by_id(doc_id: int):
    result = client.query(
        "SELECT id, name, email FROM search_docs WHERE id = {id:UInt32}",
        parameters={"id": doc_id},
    )
    if not result.result_rows:
        return None
    row = result.result_rows[0]
    return {"id": row[0], "name": row[1], "email": row[2]}


def add_doc(doc: SearchDoc):
    embedding = _embed_text(_embedding_text(doc.name, doc.email))
    _insert_vector(doc.id, doc.name, doc.email, embedding)
    return {"message": "Search doc added successfully"}


def get_all_docs():
    result = client.query("SELECT id, name, email FROM search_docs ORDER BY id")
    return [{"id": row[0], "name": row[1], "email": row[2]} for row in result.result_rows]


def get_doc_by_id(doc_id: int):
    doc = _fetch_vector_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Search doc not found")
    return doc


def delete_doc(doc_id: int):
    existing = _fetch_vector_by_id(doc_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Search doc not found")

    _delete_vector(doc_id)
    return {"message": "Search doc deleted successfully"}


def search_docs(query: str, top_k: int = 10, threshold: float = 0.5):
    """
    cosineDistance() returns 0 for an identical vector and up to 2 for a
    completely opposite one, so `1 - distance` turns it back into a
    familiar 0-1 "similarity score" (1 = perfect match).
    """
    embedding = _embed_text(query)
    result = client.query(
        """
        SELECT id, name, email,
               1 - cosineDistance(embedding, {query_embedding:Array(Float32)}) AS score
        FROM search_docs
        ORDER BY score DESC
        LIMIT {top_k:UInt32}
        """,
        parameters={"query_embedding": embedding, "top_k": top_k},
    )

    return [
        {"id": row[0], "name": row[1], "email": row[2], "score": round(row[3], 4)}
        for row in result.result_rows
        if row[3] >= threshold
    ]