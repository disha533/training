# controllers/student_controller.py


from fastapi import APIRouter
from schemas.schema import Student
from services import student_service as service

router = APIRouter(prefix="/students", tags=["STUDENT APIS"],)


@router.post("/")
def create_student(student: Student):
    return service.add_student(student)


@router.get("/")
def get_students():
    return service.get_all_students()


@router.get("/{student_id}")
def get_student(student_id: int):
    return service.get_student_by_id(student_id)


@router.put("/{student_id}")
def update_student(student_id: int, student: Student):
    return service.update_student(student_id, student)


@router.delete("/{student_id}")
def delete_student(student_id: int):
    return service.delete_student(student_id)
