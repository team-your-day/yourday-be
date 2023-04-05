from typing import Optional

from pydantic import BaseModel, Field


class CreateChatRequest(BaseModel):
    thread_id: Optional[str] = Field(description="대화 쓰레드 UUID (대화 문맥을 유지하기 위해 사용). null이라면 채팅 시작")
    content: str = Field(description="대화 내용")

    class Config:
        schema_extra = {
            "example": {
                "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
                "content": "응 방송에도 소개돼서 사람이 더 많이 몰렸나 봐 갈비찜이 맛있더라.",
            }
        }
