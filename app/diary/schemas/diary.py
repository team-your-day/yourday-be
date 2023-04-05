from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DiarySchema(BaseModel):
    id: int
    user_id: int
    content: str
    thread_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
