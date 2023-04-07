import datetime
from typing import Optional, List

import openai as openai

from app.chat.models.chat import Chat
from app.chat.repositories.chat import ChatRepository
from app.diary.models.diary import Diary
from app.diary.repositories.diary import DiaryRepository
from app.diary.schemas.diary import DiarySchema
from app.user.enums.user import InterviewTypeEnum
from app.user.models.user import User
from app.user.repositories.user import UserRepository
from core.db import Transactional
from core.utils.timezone import kst_now


class DiaryService:
    def __init__(self):
        self.diary_repo = DiaryRepository(Diary)
    async def get_diary(self, user_id: int, month: int, day: int):
        return await self.diary_repo.get_diary(user_id, month, day)
