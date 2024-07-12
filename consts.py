

class STATUS:
    PENDING = "PENDING"
    STARTED = "STARTED"
    ENDED = "ENDED"
    CANCELLED = "CANCELLED"

    CHOICES = (
        (PENDING, ("Pending")),
        (STARTED, ("Started")),
        (ENDED, ("Ended")),
        (CANCELLED, ("Canceled")),
    )


class OUTCOME:
    UNSETTLED = "UNSETTLED"
    VOID = "VOID"
    LOSE = "LOSE"
    WIN = "WIN"

    CHOICES = (
        (UNSETTLED, ("Unsettled")),
        (VOID, ("Void")),
        (LOSE, ("Lose")),
        (WIN, ("Win")),
    )