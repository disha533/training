# db/chromadb.py
#
# ONLY responsibility: connect to ChromaDB and make sure the
# search_docs collection exists.
#
# No embedding/search/business logic here.

import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="search_docs",
    metadata={"hnsw:space": "cosine"}
)