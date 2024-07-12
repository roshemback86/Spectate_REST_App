from pydantic import BaseModel
from consts import STATUS, OUTCOME

# TODO: Проверить какие нужно использовать типы на строках 16, 17 и 25

from decimal import Decimal

class Sport(BaseModel):
    name: str
    slug: str
    active: bool

class Event(BaseModel):
    name: str
    slug: str
    active: bool
    type: str
    sport: str
    status: STATUS.CHOICES
    scheduled_start: str
    actual_start: str
    logos: str


class Selection(BaseModel):
    name: str
    event: str
    active: bool
    price: Decimal
    outcome: OUTCOME.CHOICES


class ErrorMessage(BaseModel):
    pass

ErrorMessage = str()
DateTime = str()
