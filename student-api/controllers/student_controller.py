
from fastapi import APIRouter, Depends
from schemas.schema import Student, StudentUpdate
from vector_store import search_students_vector   
from services.service import (
    add_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student
)
from auth import verify_api_key

router = APIRouter(
    prefix="/students",
    dependencies=[Depends(verify_api_key)]   
)

@router.post("/")
def create_student(student: Student):
    return add_student(student)

@router.get("/")
def get_students():
    return get_all_students()

@router.get("/{student_id}")
def get_student(student_id: int):
    return get_student_by_id(student_id)

@router.patch("/{student_id}")
def update(student_id: int, student: StudentUpdate):
    return update_student(student_id, student)

@router.delete("/{student_id}")
def delete(student_id: int):
    return delete_student(student_id)

@router.get("/search/")
def search(query: str, threshold: float = 0.5):
    return search_students_vector(query, threshold=threshold)