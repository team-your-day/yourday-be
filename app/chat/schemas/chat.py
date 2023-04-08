from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatSchema(BaseModel):
    id: int = Field(description="chat ID")
    user_id: int = Field(description="유저 ID")
    content: str = Field(description="대화 내용")
    is_ai: bool = Field(description="AI가 보낸 메시지인지 여부")
    saved_at: date = Field(description="채팅을 저장할 일자")
    created_at: Optional[datetime] = Field(description="생성 일시")

    class Config:
        orm_mode = True
