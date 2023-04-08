from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field


class DiarySchema(BaseModel):
    id: int
    user_id: int
    content: str
    saved_at: date
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
