import datetime
from typing import Optional, List

import openai as openai

from app.chat.models.chat import Chat
from app.chat.repositories.chat import ChatRepository
from app.chat.schemas.chat import ChatSchema
from app.diary.models.diary import Diary
from app.diary.repositories.diary import DiaryRepository
from app.diary.schemas.diary import DiarySchema
from app.user.enums.user import InterviewTypeEnum, ToneEnum
from app.user.models.user import User
from app.user.repositories.user import UserRepository
from core.config import config
from core.db import Transactional
from core.utils.gpt_summary import summary
from core.utils.timezone import kst_now


class DiaryService:
    def __init__(self):
        self.gpt_key = config.GPT_KEY

        self.user_repo = UserRepository(User)
        self.chat_repo = ChatRepository(Chat)
        self.diary_repo = DiaryRepository(Diary)

    async def create_diary_from_openai(
        self,
        nickname: str,
        tone: ToneEnum,
        summarized_sentence: str,
    ) -> str:
        openai.api_key = self.gpt_key
        messages = [
            {
                'role': 'system',
                'content': f'''
From now on, You`re name is {nickname}. I want you to act like me. Write me a diary based on my answer before. 
Don't describe the post and your analysis and introduce yourself. Write on informal languages. 
Be {tone.value} tone. Have an empathy on my emotion. Write in Korean.
                '''
            },
            {
                'role': 'user',
                'content': f'{summarized_sentence}'
            },
        ]

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=800,
            )
        except Exception as e:
            print(f"OpenAI API request failed: {e}")
            raise e

        return completion.choices[0].message.content

    async def get_diary(self, user_id: int, month: int, day: int):
        return await self.diary_repo.get_diary(user_id, month, day)

    @Transactional()
    async def create_diary(self, user_id: int, month: int, day: int) -> Optional[DiarySchema]:
        user = await self.user_repo.get_user(user_id)
        chat_histories = await self.chat_repo.get_chat_histories(user_id, month, day)

        if not user:
            return None
        if not chat_histories:
            return None

        summarized_sentence = await summary(chat_histories)
        diary_content = await self.create_diary_from_openai(
            user.nickname,
            user.tone,
            summarized_sentence,
        )

        saved_at = datetime.date(year=kst_now().year, month=month, day=day)
        return await self.diary_repo.create_diary(
            user_id,
            diary_content,
            saved_at,
        )

    @Transactional()
    async def update_diary(self, user_id: int, month: int, day: int, content: str) -> Optional[DiarySchema]:
        return await self.diary_repo.update_diary(user_id, month, day, content)
