# backfill_vectors.py
from database import get_cursor
from vector_store import upsert_student_vector

with get_cursor() as cursor:
    cursor.execute("SELECT ID, NAME, EMAIL FROM STUDENTS")
    for id_, name, email in cursor.fetchall():
        upsert_student_vector(id_, name, email)

print("Backfill complete.")