from database import connection
from schemas.schema import Student


def add_student(student: Student):
    cursor = connection.cursor()

    query = """
        INSERT INTO STUDENTS (ID, NAME, AGE, EMAIL, BRANCH, YEAR)
        VALUES (:1, :2, :3, :4, :5, :6)
    """
    cursor.execute(query, (
        student.id,
        student.name,
        student.age,
        student.email,
        student.branch,
        student.year
    ))

    connection.commit()
    cursor.close()

    return {"message": "Student added successfully"}


def get_all_students():
    cursor = connection.cursor()

    query = "SELECT * FROM STUDENTS"

    cursor.execute(query)

    students = cursor.fetchall()

    cursor.close()

    return students


def get_student_by_id(student_id: int):
    cursor = connection.cursor()

    query = "SELECT * FROM STUDENTS WHERE ID = :1"

    cursor.execute(query, (student_id,))

    student = cursor.fetchone()

    cursor.close()

    if student:
        return student

    return {"message": "Student not found"}


def update_student(student_id: int, student: Student):
    cursor = connection.cursor()

    query = """
        UPDATE STUDENTS
        SET NAME = :1,
            AGE = :2,
            EMAIL = :3,
            BRANCH = :4,
            YEAR = :5
        WHERE ID = :6
    """

    cursor.execute(query, (
        student.name,
        student.age,
        student.email,
        student.branch,
        student.year,
        student_id
    ))

    connection.commit()
    cursor.close()

    return {"message": "Student updated successfully"}


def delete_student(student_id: int):
    cursor = connection.cursor()

    query = "DELETE FROM STUDENTS WHERE ID = :1"

    cursor.execute(query, (student_id,))

    connection.commit()
    cursor.close()

    return {"message": "Student deleted successfully"}