from sqlalchemy.orm import Session

from models.course import Course
from models.student import Student
from repositories import student_repository
from schemas.student import StudentCreate
from services.exceptions import DuplicateEmailError, NotFoundError


def create_student(db: Session, data: StudentCreate) -> Student:
    if student_repository.get_by_email(db, data.email) is not None:
        raise DuplicateEmailError(f"A student with email '{data.email}' already exists")
    return student_repository.create(db, data)


def get_student_courses(db: Session, student_id: int) -> list[Course]:
    if student_repository.get_by_id(db, student_id) is None:
        raise NotFoundError(f"Student {student_id} not found")
    return student_repository.get_enrolled_courses(db, student_id)


def get_most_enrolled_students(db: Session) -> list[tuple[Student, int]]:
    results = student_repository.get_most_enrolled(db)
    if not results:
        return []
    max_count = results[0][1]
    return [row for row in results if row[1] == max_count]
