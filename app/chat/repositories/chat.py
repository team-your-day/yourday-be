from datetime import date
from typing import Optional, List

from pydantic import parse_obj_as
from sqlalchemy import select

from app.chat.schemas.chat import ChatSchema
from core.db import session
from core.repository.base import BaseRepo
from core.utils.timezone import kst_now


class ChatRepository(BaseRepo):

    async def get_chat_histories(self, user_id: int, month: int, day: int) -> List[ChatSchema]:
        query = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.saved_at == date(kst_now().year, month, day),
            )
        )
        query = await session.execute(query)
        chat_histories = query.scalars().all()
        return parse_obj_as(List[ChatSchema], chat_histories)

    async def create_chat(
        self, user_id: int, saved_at: date, content: str, is_ai=False
    ) -> Optional[ChatSchema]:
        _model = self.model(
            user_id=user_id,
            saved_at=saved_at,
            content=content,
            is_ai=is_ai,
        )

        session.add(_model)
        await session.flush()
        return ChatSchema.from_orm(_model)
