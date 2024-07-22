from enum import Enum


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    ENDED = "ENDED"
    CANCELLED = "CANCELLED"


class OutcomeEnum(str, Enum):
    UNSETTLED = "UNSETTLED"
    VOID = "VOID"
    LOSE = "LOSE"
    WIN = "WIN"
