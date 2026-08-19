# services/course_service.py
#
# Combines what was repository + service logic: talks directly to
# CourseModel via SQLAlchemy session, and raises HTTPExceptions for
# the controller layer. No separate course_repository.py.

from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.schema import Course
from models.course import CourseModel


def add_course(db_session: Session, course: Course):
    data = course.model_dump()
    new_course = CourseModel(**data)
    db_session.add(new_course)
    db_session.commit()
    return new_course


def get_all_courses(db_session: Session):
    return db_session.query(CourseModel).all()


def get_course_by_id(db_session: Session, course_id: int):
    course =  db_session.get(CourseModel, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def update_course(db_session: Session, course_id: int, course: Course):
    data = course.model_dump()
    try:
        rows_affected = (
            db_session.query(CourseModel).filter(CourseModel.id == course_id).update(data)
        )
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"A course with id {data.get('id')} already exists",
        )

    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course updated successfully"}


def delete_course(db_session: Session, course_id: int):
    rows_affected = (
        db_session.query(CourseModel).filter(CourseModel.id == course_id).delete()
    )
    db_session.commit()
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}