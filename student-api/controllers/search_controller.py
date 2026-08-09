# controllers/search_controller.py
#
# Routes only, same pattern as student_controller.py. This router owns
# a completely separate resource - "search docs" in ClickHouse - with
# its own id space. It never touches Oracle or the students router.

from fastapi import APIRouter
from schemas.schema import SearchDoc
from services import search_service as service

router = APIRouter(prefix="/search-docs")


@router.post("/")
def create_doc(doc: SearchDoc):
    return service.add_doc(doc)


@router.get("/")
def get_docs():
    return service.get_all_docs()


@router.get("/search")
def search_docs(query: str, top_k: int = 10, threshold: float = 0.5):
    return service.search_docs(query, top_k=top_k, threshold=threshold)


@router.get("/{doc_id}")
def get_doc(doc_id: int):
    return service.get_doc_by_id(doc_id)



@router.delete("/{doc_id}")
def delete_doc(doc_id: int):
    return service.delete_doc(doc_id)
