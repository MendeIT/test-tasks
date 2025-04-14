import re
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator


class TableBaseSchema(BaseModel):
    name: str = Field(..., max_length=32)
    seats: int = Field(..., ge=1, le=1000)
    location: str = Field(..., max_length=64)

    @field_validator('name', 'location', mode='after')
    @classmethod
    def name_cannot_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                'Название, место расположение стола не может быть пустым'
            )

        if not re.fullmatch(r'^[А-Яа-яЁё0-9\s\-]+$', value.strip()):
            raise ValueError(
                'Название, место расположение стола должно содержать '
                'сивмолы кирилицы, пробелы или дефис.'
            )

        return value

    @model_validator(mode='after')
    def check_unique_table(self) -> Self:
        if self.name.lower() == self.location.lower():
            raise ValueError(
                'Название и расположение стола не может быть одинаковым'
            )

        return self


class TableCreateSchema(TableBaseSchema):
    pass


class TableReadSchema(TableBaseSchema):
    table_id: int
