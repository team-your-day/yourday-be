from typing import Optional

from sqlalchemy import select

from app.user.enums.user import ToneEnum, InterviewTypeEnum
from app.user.models.user import User
from app.user.schemas.user import UserSchema
from core.db import session
from core.repository.base import BaseRepo


class UserRepository(BaseRepo):
    async def get_user(self, user_id: int) -> Optional[UserSchema]:
        query = select(self.model).where(self.model.id == user_id)
        query = await session.execute(query)
        user = query.scalars().first()

        if not user:
            return None
        return UserSchema.from_orm(user)

    async def get_user_by_user_hash(self, user_hash: str) -> Optional[UserSchema]:
        query = select(self.model).where(self.model.user_hash == user_hash)
        query = await session.execute(query)
        user = query.scalars().first()

        if not user:
            return None
        return UserSchema.from_orm(user)

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
        query = select(self.model).where(self.model.id == user_id)
        query = await session.execute(query)
        user = query.scalars().first()

        if name:
            user.name = name
        if nickname:
            user.nickname = nickname
        if tone:
            user.tone = tone.value
        if interview:
            user.interview = interview.value

        session.add(user)
        await session.flush()
        return UserSchema.from_orm(user)
