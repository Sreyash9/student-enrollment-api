from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    title: str
    description: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
