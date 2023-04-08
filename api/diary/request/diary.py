from typing import Optional

from pydantic import BaseModel, Field

from app.user.enums.user import ToneEnum, InterviewTypeEnum
from core.utils.all_optional import AllOptional


class UpdateDiaryRequestSerializer(BaseModel):
    content: str = Field(..., description="수정할 일기 본문")

    class Config:
        schema_extra = {
            "example": {
                "content": "오늘 맛집에 갔는데 사람이 많았어.",
            }
        }
