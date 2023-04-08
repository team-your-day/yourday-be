from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CreateChatRequest(BaseModel):
    saved_at: date = Field(description="저장할 날짜")
    content: str = Field(description="대화 내용")

    class Config:
        schema_extra = {
            "example": {
                "saved_at": "2023-04-08",
                "content": "응 방송에도 소개돼서 사람이 더 많이 몰렸나 봐 갈비찜이 맛있더라.",
            }
        }
