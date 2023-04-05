from typing import Optional

from pydantic import BaseModel, Field

from app.user.enums.user import ToneEnum, InterviewTypeEnum
from core.utils.all_optional import AllOptional


class SaveUserInfoRequest(BaseModel):
    name: str = Field(description="사용자 이름")
    nickname: str = Field(description="Ai 닉네임")
    tone: ToneEnum = Field(description="어투 (활기, 차분)")
    interview: InterviewTypeEnum = Field(description="인터뷰 방식 (얕고 많이, 깊고 적게)")

    class Config:
        schema_extra = {
            "example": {
                "name": "yunjae",
                "nickname": "ai nickname",
                "tone": "calm",
                "interview": "low",
            }
        }


class UpdateUserInfoRequest(SaveUserInfoRequest, metaclass=AllOptional):
    class Config:
        schema_extra = {
            "example": {
                "name": "yunjae",
                "nickname": "ai nickname",
                "tone": "calm",
                "interview": "low",
            }
        }
