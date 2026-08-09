# services/student_service.py

from fastapi import HTTPException
from schemas.schema import Student
from db.oracle import get_cursor


def add_student(student: Student):
    data = student.model_dump()
    columns = ", ".join(col.upper() for col in data.keys())
    placeholders = ", ".join(f":{col}" for col in data.keys())
    query = f"INSERT INTO STUDENTS ({columns}) VALUES ({placeholders})"

    with get_cursor(commit=True) as cursor:
        cursor.execute(query, data)

    return {"message": "Student added successfully"}


def get_all_students():
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM STUDENTS")
        return cursor.fetchall()


def get_student_by_id(student_id: int):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM STUDENTS WHERE ID = :id", {"id": student_id})
        student = cursor.fetchone()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def update_student(student_id: int, student: Student):
    # PUT, not PATCH: the caller must send every field every time, so we
    # always overwrite the whole row. No "partial update" branch to
    # maintain, no exclude_unset bookkeeping.
    data = student.model_dump()
    set_clause = ", ".join(f"{col.upper()} = :{col}" for col in data.keys())
    query = f"UPDATE STUDENTS SET {set_clause} WHERE ID = :id"

    with get_cursor(commit=True) as cursor:
        cursor.execute(query, {**data, "id": student_id})
        rows_affected = cursor.rowcount

    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}


def delete_student(student_id: int):
    with get_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM STUDENTS WHERE ID = :id", {"id": student_id})
        rows_affected = cursor.rowcount

    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}