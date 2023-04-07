from datetime import date
from typing import Optional, List

from pydantic import parse_obj_as
from sqlalchemy import select

from app.diary.schemas.diary import DiarySchema
from app.user.enums.user import ToneEnum, InterviewTypeEnum
from app.user.models.user import User
from app.user.schemas.user import UserSchema
from core.db import session
from core.repository.base import BaseRepo


class DiaryRepository(BaseRepo):
    async def get_diary(self, user_id: int, month: int, day: int = 0) -> List[DiarySchema]:
        query = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.month == month,
            )
        )
        if day:
            query = query.where(self.model.day == day)
        query = await session.execute(query)
        diary = query.scalars().all()

        if not diary:
            return []
        return parse_obj_as(List[DiarySchema], diary)

    async def save_user(
        self,
        user_hash: str,
        name: str,
        nickname: str,
        tone: ToneEnum,
        interview: InterviewTypeEnum,
    ) -> UserSchema:
        _model = User(
            user_hash=user_hash,
            name=name,
            nickname=nickname,
            tone=tone.value,
            interview=interview.value,
        )

        session.add(_model)
        await session.flush()
        return UserSchema.from_orm(_model)

    async def update_user_info(
        self,
        user_id: int,
        name: Optional[str],
        nickname: Optional[str],
        tone: Optional[ToneEnum],
        interview: Optional[InterviewTypeEnum],
    ) -> Optional[UserSchema]:
        user = await self.get_user(user_id)
        if not user:
            return None

        if not name:
            user.name = name
        if not nickname:
            user.nickname = nickname
        if not tone:
            user.tone = tone
        if not interview:
            user.interview = interview

        session.add(user)
        await session.flush()
        return UserSchema.from_orm(user)
