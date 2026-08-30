from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.enrollment import Enrollment
from repositories import course_repository, enrollment_repository, student_repository
from schemas.enrollment import EnrollmentCreate
from services.exceptions import (
    CapacityExceededError,
    DuplicateEnrollmentError,
    NotFoundError,
)
from utils.constants import MAX_STUDENTS_PER_COURSE


def create_enrollment(db: Session, data: EnrollmentCreate) -> Enrollment:
    if student_repository.get_by_id(db, data.student_id) is None:
        raise NotFoundError(f"Student {data.student_id} not found")

    if course_repository.get_by_id(db, data.course_id) is None:
        raise NotFoundError(f"Course {data.course_id} not found")

    if enrollment_repository.exists(db, data.student_id, data.course_id):
        raise DuplicateEnrollmentError("Student is already enrolled in this course")

    current_count = enrollment_repository.count_for_course(db, data.course_id)
    if current_count >= MAX_STUDENTS_PER_COURSE:
        raise CapacityExceededError(
            f"Course has reached the maximum capacity of {MAX_STUDENTS_PER_COURSE} students"
        )

    enrollment = enrollment_repository.create(db, data.student_id, data.course_id)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEnrollmentError("Student is already enrolled in this course")
    db.refresh(enrollment)
    return enrollment


def delete_enrollment(db: Session, enrollment_id: int) -> None:
    enrollment = enrollment_repository.get_by_id(db, enrollment_id)
    if enrollment is None:
        raise NotFoundError(f"Enrollment {enrollment_id} not found")
    enrollment_repository.delete(db, enrollment)
