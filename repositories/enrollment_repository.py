from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.enrollment import Enrollment


def create(db: Session, student_id: int, course_id: int) -> Enrollment:
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    return enrollment


def get_by_id(db: Session, enrollment_id: int) -> Enrollment | None:
    return db.get(Enrollment, enrollment_id)


def exists(db: Session, student_id: int, course_id: int) -> bool:
    stmt = select(Enrollment.id).where(
        Enrollment.student_id == student_id, Enrollment.course_id == course_id
    )
    return db.scalar(stmt) is not None


def count_for_course(db: Session, course_id: int) -> int:
    stmt = select(func.count(Enrollment.id)).where(Enrollment.course_id == course_id)
    return db.scalar(stmt) or 0


def delete(db: Session, enrollment: Enrollment) -> None:
    db.delete(enrollment)
    db.commit()
