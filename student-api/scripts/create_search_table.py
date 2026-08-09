# scripts/create_search_table.py
#
# Run once, manually, to create the search_docs table in ClickHouse:
#   python -m scripts.create_search_table
#
# Mirrors scripts/create_table.py (which does the same for Oracle's
# STUDENTS table). Kept as two separate scripts on purpose - there is
# no "run both at once" step, because the two stores are unrelated.

from db.clickhouse import init_vector_table

init_vector_table()
print("search_docs table created successfully!")
