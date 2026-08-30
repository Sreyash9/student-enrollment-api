from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from models.course import Course
from models.enrollment import Enrollment
from models.student import Student
from schemas.student import StudentCreate


def create(db: Session, data: StudentCreate) -> Student:
    student = Student(name=data.name, email=data.email)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_by_id(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def get_by_email(db: Session, email: str) -> Student | None:
    return db.scalar(select(Student).where(Student.email == email))


def get_enrolled_courses(db: Session, student_id: int) -> list[Course]:
    stmt = select(Course).join(Enrollment).where(Enrollment.student_id == student_id)
    return list(db.scalars(stmt).all())


def get_most_enrolled(db: Session) -> list[tuple[Student, int]]:
    count_col = func.count(Enrollment.id).label("cnt")
    stmt = (
        select(Student, count_col)
        .join(Enrollment)
        .group_by(Student.id)
        .order_by(desc(count_col))
    )
    return [(row[0], row[1]) for row in db.execute(stmt).all()]
