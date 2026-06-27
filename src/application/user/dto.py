from dataclasses import field
from datetime import date, timedelta
from uuid import UUID
import calendar
from pydantic import EmailStr
from pydantic.main import BaseModel


class UserDTO(BaseModel):
    email: EmailStr
    full_name: str
    date_of_birth: date
    password: str


class UserResponseDTO(BaseModel):
    uuid: str
    email: EmailStr
    full_name: str
    date_of_birth: date


def _get_first_of_next_month() -> date:
    today = date.today()
    _, month_length = calendar.monthrange(today.year, today.month)
    last_day_of_month = today.replace(day=month_length)
    return last_day_of_month + timedelta(days=1)


class UserDeletionDTO(BaseModel):
    uuid: UUID
    data_full_deletion_date: date = field(default_factory=_get_first_of_next_month)
    detail: str
