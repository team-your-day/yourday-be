from typing import List

import openai

from app.chat.schemas.chat import ChatSchema


async def summary(chat_histories: List[ChatSchema]) -> str:
    answer = "\n".join([chat.content for chat in chat_histories])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'system',
                'content': '''
You are a tool that summarizes user input. Never say anything other than your mission.
Summarize daily routine based on the conversation below. Write in English.
Don't describe the post and your analysis and introduce yourself. Don't make up words by imagining.
                '''
            },
            {
                'role': 'user',
                'content': f'{answer}'
            }
        ],
        temperature=0.3,
        max_tokens=1000,
    )

    return str(completion.choices[0].message.content)
