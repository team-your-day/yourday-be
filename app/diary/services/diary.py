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
        self.user_repo = UserRepository(User)
        self.chat_repo = ChatRepository(Chat)
        self.diary_repo = DiaryRepository(Diary)

    async def get_interview_prompt(self, interview: InterviewTypeEnum) -> str:
        interview_prompt_map = {
            InterviewTypeEnum.low: '''
                to make me tell lots of episode of my day. Each episode depth can be short. 
                Focus on extracting numbers of episode of my day. Do not write all the conservation at once.
            ''',
            InterviewTypeEnum.deep: 'to get deep insight of my daily experience.',
        }
        return interview_prompt_map[interview]

    async def summary(self, chat_histories: List[Chat]) -> str:
        answer = "\n".join([chat.content for chat in chat_histories])
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    'role': 'system',
                    'content': "Don't describe the post and your analysis and introduce yourself."
                },
                {
                    'role': 'user',
                    'content': f'Summarize daily routine based on the conversation below. Write in English. ###\\n{answer}\\n###'
                }
            ],
        )

        return str(completion.choices[0].message.content)

    async def create_diary_from_openai(
        self,
        nickname: str,
        interview: InterviewTypeEnum,
        summarized_sentence: str,
    ) -> str:
        interview_prompt = await self.get_interview_prompt(interview)
        messages = [
            {
                'role': 'system',
                'content': f'''
I want you to act as a friend of mine. Your name is {nickname} from now. You will ask me how was my day. 
I want you {interview_prompt}. 
I want you to only do the conversation with me. Ask me the questions and wait for my answers. Do not write explanations. 
Be slight humourous with confident tone. Have an empathy on my emotion. Write in Korean.
                '''
            },
            {
                'role': 'user',
                'content': f'Write a diary in Korean. ###\\n{summarized_sentence}\\n###'
            },
            {
                'role': 'assistant',
                'content': summarized_sentence
            }
        ]

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
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

        summarized_sentence = await self.summary(chat_histories)
        diary_content = await self.create_diary_from_openai(
            user.nickname,
            user.interview,
            summarized_sentence,
        )

        saved_at = datetime.date(year=kst_now().year, month=month, day=day)
        return await self.diary_repo.create_diary(
            user_id,
            diary_content,
            saved_at,
        )

    @Transactional()
    async def update_diary(self, user_id: int, month: int, day: int, content: str):
        return await self.diary_repo.update_diary(user_id, month, day, content)
