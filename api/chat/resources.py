from fastapi import APIRouter, Path, Response, Depends, Body
from starlette.requests import Request

from api.chat.request.chat import CreateChatRequest
from api.chat.response.chat import ChatListResponse, ChatResponse
from api.diary.response.diary import DiaryResponse, DiaryListResponse
from app.chat.services.chat import ChatService
from core.exceptions import BadRequestException, UnauthorizedException
from core.exceptions.schema import ExceptionResponseSchema
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.utils.timezone import kst_now

chat_router = APIRouter()


@chat_router.get(
    "/{month}/{day}",
    response_model=ChatListResponse,
    response_model_include=ChatListResponse.Config.include,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="chat history 조회 API",
)
async def get_chat_list(request: Request):
    return {
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
    # chat_service = ChatService()
    # chat_list = await chat_service.get_chat_list(request.user.id)
    # return {"chat": chat_list}


@chat_router.post(
    "/{month}/{day}",
    response_model=ChatResponse,
    response_model_include=ChatResponse.Config.include,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="chat 생성 API",
)
async def create_chat(
    request: Request,
    body: CreateChatRequest,
):
    return {
        "chat": {
            "id": 2,
            "user_id": 1,
            "content": "오늘 맛집에 갔는데 사람이 많았어.",
            "is_ai": True,
            "saved_at": "2023-04-08",
        }
    }
