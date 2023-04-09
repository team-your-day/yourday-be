from datetime import date

import openai

from app.chat.models.chat import Chat
from app.chat.repositories.chat import ChatRepository
from app.user.enums.user import InterviewTypeEnum, ToneEnum
from app.user.models.user import User
from app.user.repositories.user import UserRepository
from core.config import config
from core.db import Transactional
from core.utils.gpt_summary import summary
from core.utils.timezone import kst_now


class ChatService:
    def __init__(self):
        self.gpt_key = config.GPT_KEY

        self.user_repo = UserRepository(User)
        self.chat_repo = ChatRepository(Chat)

    async def get_interview_prompt(self, interview: InterviewTypeEnum) -> str:
        interview_prompt_map = {
            InterviewTypeEnum.low: '''
to make me tell lots of episode of my day. Each episode depth can be short. 
Focus on extracting numbers of episode of my day. Do not write all the conservation at once.
            ''',
            InterviewTypeEnum.deep: 'to get deep insight of my daily experience.',
        }
        return interview_prompt_map[interview]

    async def get_chat_list(self, user_id: int, month: int, day: int):
        return await self.chat_repo.get_chat_histories(user_id, month, day)

    @Transactional()
    async def create_chat(self, user_id: int, month: int, day: int, content: str):
        user = await self.user_repo.get_user(user_id)
        if not user:
            return None

        saved_at = date(kst_now().year, month, day)
        await self.chat_repo.create_chat(user_id, saved_at, content)

        openai.api_key = self.gpt_key
        chat_histories = await self.chat_repo.get_chat_histories(user_id, month, day)
        summarized_sentence = ''
        if chat_histories:
            summarized_sentence = await summary(chat_histories)

        gpt_reply = await self.create_gpt_reply(
            user_id, month, day, content, user.nickname, user.interview, user.tone, summarized_sentence
        )
        return await self.chat_repo.create_chat(user_id, saved_at, gpt_reply, is_ai=True)

    async def create_gpt_reply(
        self,
        user_id: int,
        month: int,
        day: int,
        content: str,
        nickname: str,
        interview: InterviewTypeEnum,
        tone: ToneEnum,
        summarized_sentence: str,
    ):
        openai.api_key = self.gpt_key
        interview_prompt = await self.get_interview_prompt(interview)
        messages = [
            {
                'role': 'system',
                'content': f'''
I want you to act as a friend of mine. Your name is {nickname} from now. You will ask me how was my day. 
I want you {interview_prompt}. 
I want you to only do the conversation with me. Ask me the questions and wait for my answers. Do not write explanations. 
Be {tone.value} tone. Have an empathy on my emotion.
                '''
            },
            {
                'role': 'user',
                'content': f'{content}'
            },
            {
                'role': 'assistant',
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


