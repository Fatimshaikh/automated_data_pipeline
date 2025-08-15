from pydantic import BaseModel
from datetime import datetime

class DataItemCreate(BaseModel):
    name: str
    value: float

class DataItemResponse(BaseModel):
    id: int
    name: str
    value: float
    created_at: datetime

    class Config:
        orm_mode = True
