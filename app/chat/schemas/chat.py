from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatSchema(BaseModel):
    id: int = Field(description="chat ID")
    user_id: int = Field(description="유저 ID")
    thread_id: str = Field(description="대화 쓰레드 UUID (대화 문맥을 유지하기 위해 사용)")
    content: str = Field(description="대화 내용")
    is_ai: bool = Field(description="AI가 보낸 메시지인지 여부")
    created_at: datetime = Field(description="생성 일시")

    class Config:
        orm_mode = True
