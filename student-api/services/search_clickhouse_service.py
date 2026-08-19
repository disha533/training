#
# Talks directly to ClickHouse. It has no idea Oracle or students exist -
# search docs are their own dataset, created and managed through their
# own endpoints, not derived from student data.
#
#   controller -> service (this file) -> db

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


def add_doc(doc: SearchDoc):
    embedding = _embed_text(_embedding_text(doc.name, doc.email))

    client.insert(
        "search_docs",
        [[doc.id, doc.name, doc.email, embedding]],
        column_names=["id", "name", "email", "embedding"],
    )

    return {"message": "Search doc added successfully"}


def search_docs(query: str, top_k: int = 10, threshold: float = 0.5):
   
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