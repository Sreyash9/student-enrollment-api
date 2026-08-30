from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.course import Course
from models.enrollment import Enrollment
from models.student import Student
from schemas.course import CourseCreate
from utils.constants import POPULAR_COURSE_THRESHOLD


def create(db: Session, data: CourseCreate) -> Course:
    course = Course(title=data.title, description=data.description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_by_id(db: Session, course_id: int) -> Course | None:
    return db.get(Course, course_id)


def get_enrolled_students(db: Session, course_id: int) -> list[Student]:
    stmt = select(Student).join(Enrollment).where(Enrollment.course_id == course_id)
    return list(db.scalars(stmt).all())


def get_popular(db: Session, min_count: int = POPULAR_COURSE_THRESHOLD) -> list[tuple[Course, int]]:
    count_col = func.count(Enrollment.id).label("cnt")
    stmt = (
        select(Course, count_col)
        .join(Enrollment)
        .group_by(Course.id)
        .having(count_col > min_count)
        .order_by(count_col.desc())
    )
    return [(row[0], row[1]) for row in db.execute(stmt).all()]


def get_empty(db: Session) -> list[Course]:
    stmt = select(Course).outerjoin(Enrollment).where(Enrollment.id.is_(None))
    return list(db.scalars(stmt).all())
