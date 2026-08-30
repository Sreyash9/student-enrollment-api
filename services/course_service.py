from sqlalchemy.orm import Session

from models.course import Course
from models.student import Student
from repositories import course_repository
from schemas.course import CourseCreate
from services.exceptions import NotFoundError
from utils.constants import POPULAR_COURSE_THRESHOLD


def create_course(db: Session, data: CourseCreate) -> Course:
    return course_repository.create(db, data)


def get_course_students(db: Session, course_id: int) -> list[Student]:
    if course_repository.get_by_id(db, course_id) is None:
        raise NotFoundError(f"Course {course_id} not found")
    return course_repository.get_enrolled_students(db, course_id)


def get_popular_courses(db: Session, min_count: int = POPULAR_COURSE_THRESHOLD) -> list[tuple[Course, int]]:
    return course_repository.get_popular(db, min_count)


def get_empty_courses(db: Session) -> list[Course]:
    return course_repository.get_empty(db)
