from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ReservationBaseSchema(BaseModel):
    customer_name: str = Field(..., max_length=32)
    reservation_time: Optional[datetime] = None
    duration_minutes: int = Field(..., gt=0, le=300)
    table_id: int = Field(..., gt=0)

    @field_validator('customer_name', mode='after')
    @classmethod
    def name_cannot_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Имя клиента не может быть пустым')
        return v.capitalize()


class ReservationCreateSchema(ReservationBaseSchema):
    pass


class ReservationReadSchema(ReservationBaseSchema):
    reservation_id: int
