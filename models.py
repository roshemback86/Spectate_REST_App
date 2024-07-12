from  pydantic import BaseModel


class Sport(BaseModel):
    pass

class Event(BaseModel):
    pass

class Selection(BaseModel):
    pass

class ErrorMessage(BaseModel):
    pass

ErrorMessage = str()
DateTime = str()
