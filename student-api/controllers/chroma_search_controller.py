from fastapi import APIRouter
from schemas.schema import SearchDoc
from services.search_chroma_service import add_doc, search_docs

router = APIRouter(
    prefix="/chroma/search",
    tags=["Chroma Search"],
)


@router.post("/")
def create_doc(doc: SearchDoc):
    return add_doc(doc)


@router.get("/")
def search(
    query: str,
    top_k: int = 10,
    threshold: float = 0.5,
):
    return search_docs(query=query, top_k=top_k, threshold=threshold)