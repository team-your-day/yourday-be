from typing import Optional

from pydantic import BaseModel, Field

from app.user.enums.user import ToneEnum, InterviewTypeEnum


class UserSchema(BaseModel):
    id: int = Field(description="사용자 id - auto increment")
    user_hash: str = Field(description="사용자 정보 기반 고유 키값")
    name: str = Field(description="사용자 이름")
    nickname: str = Field(description="Ai 닉네임")
    tone: ToneEnum = Field(description="어투 (활기, 차분)")
    interview: InterviewTypeEnum = Field(description="인터뷰 방식 (얕고 많이, 깊고 적게)")

    class Config:
        orm_mode = True
