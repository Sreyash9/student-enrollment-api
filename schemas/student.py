from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class StudentBase(BaseModel):
    name: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
