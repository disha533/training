# controllers/chroma_search_controller.py

from fastapi import APIRouter
from schemas.schema import SearchDoc
from services.search_chroma_service import (
    add_doc,
    get_all_docs,
    get_doc_by_id,
    delete_doc,
    search_docs,
)

router = APIRouter(
    prefix="/chroma/search",
    tags=["Chroma Search"],
)


@router.post("/")
def create_doc(doc: SearchDoc):
    return add_doc(doc)


@router.get("/")
def get_docs():
    return get_all_docs()


@router.get("/{doc_id}")
def get_doc(doc_id: int):
    return get_doc_by_id(doc_id)


@router.delete("/{doc_id}")
def delete(doc_id: int):
    return delete_doc(doc_id)


@router.get("/query/search")
def search(
    query: str,
    top_k: int = 10,
    threshold: float = 0.5,
):
    return search_docs(
        query=query,
        top_k=top_k,
        threshold=threshold,
    )