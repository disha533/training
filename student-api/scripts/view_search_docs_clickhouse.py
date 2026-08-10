# scripts/view_search_docs.py
#
# Quick manual check of what's currently stored in ClickHouse:
#   python -m scripts.view_search_docs
import db
from db.clickhouse import client

result = client.query("SELECT id, name, email, length(embedding) FROM search_docs")

print(f"Total search docs stored: {len(result.result_rows)}\n")
for id_, name, email, embedding_length in result.result_rows:
    print(f"ID: {id_} | Name: {name} | Email: {email} | Embedding length: {embedding_length}")
    print("-" * 50)
