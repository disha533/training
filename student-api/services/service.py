# services/service.py
from database import get_cursor
from schemas.schema import Student, StudentUpdate
from fastapi import HTTPException
from vector_store import upsert_student_vector, delete_student_vector

def add_student(student: Student):
    data = student.model_dump()
    columns = ", ".join(col.upper() for col in data.keys())
    placeholders = ", ".join(f":{col}" for col in data.keys())
    query = f"INSERT INTO STUDENTS ({columns}) VALUES ({placeholders})"

    with get_cursor(commit=True) as cursor:
        cursor.execute(query, data)
    upsert_student_vector(data["id"], data["name"], data["email"])
    return {"message": "Student added successfully"}


def get_all_students():
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM STUDENTS")
        return cursor.fetchall()


def get_student_by_id(student_id: int):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM STUDENTS WHERE ID = :id", {"id": student_id})
        student = cursor.fetchall()

    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")


def update_student(student_id: int, student: StudentUpdate):
    data = student.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    set_clause = ", ".join(f"{col.upper()} = :{col}" for col in data.keys())
    query = f"UPDATE STUDENTS SET {set_clause} WHERE ID = :id"
    data["id"] = student_id

    with get_cursor(commit=True) as cursor:
        cursor.execute(query, data)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

    with get_cursor() as cursor:
        cursor.execute("SELECT NAME, EMAIL FROM STUDENTS WHERE ID = :id", {"id": student_id})
        name, email = cursor.fetchall()
        upsert_student_vector(student_id, name, email)

    return {"message": "Student updated successfully"}


def delete_student(student_id: int):
    with get_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM STUDENTS WHERE ID = :id", {"id": student_id})
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
    delete_student_vector(student_id)   
    return {"message": "Student deleted successfully"}