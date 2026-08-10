# controllers/course_controller.py

from fastapi import APIRouter
from db.sqlalchemydb import SessionDep
from schemas.schema import Course
from services import course_service as service

router = APIRouter(prefix="/courses")


@router.post("/")
def create_course(course: Course, db: SessionDep):
    return service.add_course(db, course)


@router.get("/")
def get_courses(db: SessionDep):
    return service.get_all_courses(db)


@router.get("/{course_id}")
def get_course(course_id: int, db: SessionDep):
    return service.get_course_by_id(db, course_id)


@router.put("/{course_id}")
def update_course(course_id: int, course: Course, db: SessionDep):
    return service.update_course(db, course_id, course)


@router.delete("/{course_id}")
def delete_course(course_id: int, db: SessionDep):
    return service.delete_course(db, course_id)