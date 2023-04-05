from fastapi import APIRouter, Path, Response, Depends, Body
from starlette.requests import Request

from api.diary.response.diary import DiaryResponse, DiaryListResponse
from core.exceptions import BadRequestException, UnauthorizedException
from core.exceptions.schema import ExceptionResponseSchema
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.utils.timezone import kst_now

diary_router = APIRouter()


@diary_router.get(
    "/{month}/{day}",
    response_model=DiaryListResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="일기 조회 API",
)
async def get_diary(request: Request):
    """
    day가 0이면 해당 month의 데이터를 전체 조회합니다.
    month는 0이 아닌 값이 들어와야 합니다.
    """
    return {
        "diary": [
            {
                "id": 1,
                "user_id": 1,
                "content": "맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다. 맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다.",
                "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
                "created_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        ]
    }


@diary_router.post(
    "/{month}/{day}",
    response_model=DiaryResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="일기 생성 API",
)
async def create_diary(
    request: Request,
    user_hash: str = Body(..., description="유저 해시값"),
):
    return {
        "diary": {
            "id": 1,
            "user_id": 1,
            "content": "맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다. 맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다.",
            "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
            "created_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    }


@diary_router.patch(
    "/{month}/{day}",
    response_model=DiaryResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    summary="일기 수정 API",
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
        401: {
            "description": UnauthorizedException.message,
            "model": ExceptionResponseSchema,
        },
    },
)
async def update_diary(
    request: Request,
    content: str = Body(..., description="수정할 일기 본문")
):
    return {
        "diary": {
            "id": 1,
            "user_id": 1,
            "content": "맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다. 맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다.",
            "thread_id": "bb743fdd-3273-44fe-9f3e-1713e0c5abe9",
            "created_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    }