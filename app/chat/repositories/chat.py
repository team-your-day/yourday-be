from typing import Optional

from sqlalchemy import select

from core.db import session
from core.repository.base import BaseRepo


class ChatRepository(BaseRepo):

    async def get_chat_histories(self, user_id, month, day):
        pass
