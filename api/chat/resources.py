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
async def get_chat_list(
    request: Request,
    month: str = Path(...),
    day: str = Path(...),
):
    chat_service = ChatService()
    chat_list = await chat_service.get_chat_list(request.user.id, int(month), int(day))
    return {"chat": chat_list}


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
    month: str = Path(...),
    day: str = Path(...),
    body: CreateChatRequest = Body(...),
):
    chat_service = ChatService()
    chat = await chat_service.create_chat(request.user.id, int(month), int(day), body.content)
    return {"chat": chat}
