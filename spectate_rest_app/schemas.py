from pydantic import BaseModel, Field
from .consts import StatusEnum, OutcomeEnum
from typing import List, Optional
from datetime import datetime
# TODO: Проверить какие типы(связи) нужно использовать типы на строках 21, 29

from decimal import Decimal


class Sport(BaseModel):
    name: str
    slug: Optional[str] = Field(None, example="football")
    active: Optional[bool] = Field(True, example=True)


class Event(BaseModel):
    name: str
    slug: Optional[str] = None
    active: Optional[bool] = True
    type: str
    sport: str
    status: StatusEnum
    scheduled_start: datetime
    actual_start: Optional[datetime] = None
    logos: Optional[str] = Field(None, example="url")


class Selection(BaseModel):
    name: str
    event: str
    active: Optional[bool] = True
    price: Decimal
    outcome: OutcomeEnum


class ErrorMessage(BaseModel):
    error_message: str

