# services/service.py
from database import get_cursor
from schemas.schema import Student, StudentUpdate
from fastapi import HTTPException

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

    return {"message": "Student updated successfully"}


def delete_student(student_id: int):
    with get_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM STUDENTS WHERE ID = :id", {"id": student_id})
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}