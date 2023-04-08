from typing import List

from pydantic import BaseModel

from app.chat.schemas.chat import ChatSchema


class ChatListResponse(BaseModel):
    chat: List[ChatSchema]

    class Config:
        include = {
            "chat": {
                "__all__": {
                    "id": ...,
                    "user_id": ...,
                    "content": ...,
                    "is_ai": ...,
                    "saved_at": ...,
                }
            }
        }
        schema_extra = {
            "example": {
                "chat": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "content": "오늘 무슨 일이 있었나요?",
                        "is_ai": True,
                        "saved_at": "2023-04-08",
                    },
                    {
                        "id": 2,
                        "user_id": 1,
                        "content": "오늘 무슨 일이 있었나요?",
                        "is_ai": False,
                        "saved_at": "2023-04-08",
                    },
                    {
                        "id": 3,
                        "user_id": 1,
                        "content": "오늘 무슨 일이 있었나요?",
                        "is_ai": True,
                        "saved_at": "2023-04-08",
                    },
                    {
                        "id": 4,
                        "user_id": 1,
                        "content": "오늘 무슨 일이 있었나요?",
                        "is_ai": False,
                        "saved_at": "2023-04-08",
                    },
                ]
            }
        }


class ChatResponse(BaseModel):
    chat: ChatSchema

    class Config:
        include = {
            "chat": {
                "id": ...,
                "user_id": ...,
                "content": ...,
                "is_ai": ...,
                "saved_at": ...,
            }
        }
        schema_extra = {
            "example": {
                "chat": {
                    "id": 2,
                    "user_id": 1,
                    "content": "오늘 맛집에 갔는데 사람이 많았어.",
                    "is_ai": True,
                    "saved_at": "2023-04-08",
                }
            }
        }
