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
                        "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
                        "content": "오늘 무슨 일이 있었나요?",
                        "is_ai": True,
                        "created_at": "2023-04-05 23:31:42",
                    },
                    {
                        "id": 2,
                        "user_id": 1,
                        "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
                        "content": "오늘 맛집에 갔는데 사람이 많았어.",
                        "is_ai": False,
                        "created_at": "2023-04-05 23:31:55",
                    },
                    {
                        "id": 3,
                        "user_id": 1,
                        "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
                        "content": "그랬군요 얼마나 맛집이길래 사람이 많았어요?",
                        "is_ai": True,
                        "created_at": "2023-04-05 23:32:14",
                    },
                    {
                        "id": 4,
                        "user_id": 1,
                        "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
                        "content": "응 방송에도 소개돼서 사람이 더 많이 몰렸나 봐 갈비찜이 맛있더라.",
                        "is_ai": False,
                        "created_at": "2023-04-05 23:32:28",
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
