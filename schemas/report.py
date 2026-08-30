from schemas.course import CourseRead
from schemas.student import StudentRead


class PopularCourseOut(CourseRead):
    enrolled_count: int


class TopStudentOut(StudentRead):
    course_count: int
